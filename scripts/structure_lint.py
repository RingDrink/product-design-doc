#!/usr/bin/env python3
"""Mechanical structure checks for product-design-doc Markdown drafts.

This linter intentionally checks only low-ambiguity structure and readability
signals. It does not judge design quality.

Usage:
    python3 structure_lint.py [--strict] draft.md
    cat draft.md | python3 structure_lint.py [--strict] -
    python3 structure_lint.py --implementation-ready requirement.md
    python3 structure_lint.py --rendered exported.md
    python3 structure_lint.py --rendered --require-numbered-headings exported.html
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass


ROLE_MARKERS = "🔴🔵🟡🟣🟠🟢"
ROLE_RE = re.compile(f"[{ROLE_MARKERS}]")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
QUOTE_RE = re.compile(r"^\s*>")
RESOURCE_HEADING_RE = re.compile(r"资源清单|Resource List|Resources", re.IGNORECASE)
HEADER_META_RE = re.compile(
    r"^\s*(Type|Status|UX|UI|UX / UI Source|Dependencies|Version|Scope|Date|Owner|"
    r"类型|状态|UX 设计案|依赖|版本|范围|日期|负责人)\s*[：:]"
)

FACET_NAMES = (
    "功能目标|玩家操作|用户行为|玩家行为|规则与反馈|限制与例外|系统响应|配置需求|资源需求|"
    "界面反馈|失败状态|判定规则|实现口径|User Action|System Response|Rules And Feedback|"
    "Limitations And Exceptions"
)
FACET_LABEL_SAMELINE_RE = re.compile(
    rf"^\s*\*\*(?:{FACET_NAMES})(?:[：:])?\*\*[：:]?\s*\S",
    re.IGNORECASE,
)
FACET_LABEL_EXACT_RE = re.compile(
    rf"^(?:\d+(?:\.\d+)*[.、]?\s*)?(?:{FACET_NAMES})[：:]?$",
    re.IGNORECASE,
)

ANCHOR_PATTERNS = [
    ("decision-id", re.compile(r"\bD-[^\s，。；;（）()、`/\\]+-\d+\b")),
    ("capture-card-id", re.compile(r"\bC-\d{8}\b")),
    ("block-id", re.compile(r"\bblk[a-zA-Z0-9]{6,}\b|\bdox[a-zA-Z0-9]{8,}\b")),
    ("wikilink", re.compile(r"\[\[[^\]]+\]\]")),
    ("abs-unix-path", re.compile(r"(?<![`\w])/Users/[^\s)`]+")),
    ("abs-windows-path", re.compile(r"\b[A-Za-z]:\\[^\s)`]+")),
    ("home-relative-path", re.compile(r"(?<![`\w])~/[^\s)`]+")),
]

BANNED_COLOR_RE = re.compile(r'<text\s+color="(gray|grey)"', re.IGNORECASE)
VISUAL_RE = re.compile(r"(<whiteboard\b|<img\b|!\[[^\]]*\]\([^)]+\))", re.IGNORECASE)
LOW_FIDELITY_UI_RE = re.compile(r"(<whiteboard\b|<svg\b|```svg\b)", re.IGNORECASE)
VISUAL_CAPTION_RE = re.compile(
    r"^\s*>\s*(?:\*\*)?(?:图|截图|参考|画板|UX 图|Figure|Screenshot|Reference|Diagram)(?:\s*\d+)?\s*[：:｜|]",
    re.IGNORECASE,
)
MARKDOWN_IMAGE_RE = re.compile(r"!\[([^\]]*)\]\([^)]+\)")
LONG_ALT_HINTS = ("图片展示", "展示的是", "该图片", "直观呈现", "相关内容", "image showing")
NONHUMAN_TERMS = {
    r"\bTip\b": "use the concrete UI/control name",
    r"\bscoping\b": "use scope / version scope",
    "系统响应": "use a business heading such as failure handling or purchase feedback",
    "玩家行为": "use a business heading such as entry and operation",
    "规则与反馈": "use concrete business subheadings",
    "限制与例外": "use scope / failure / exception headings only when meaningful",
}
FILLER_WORDS = ["此外", "综上", "值得注意的是", "该功能旨在", "确保", "提供无缝体验", "发挥关键作用"]
UNRESOLVED_HEADING_RE = re.compile(
    r"(?:冻结决策|待确认(?:项|问题)?|开放问题|未决(?:事项|问题|决策)|"
    r"open questions?|open decisions?|unresolved (?:questions?|decisions?|blockers?))",
    re.IGNORECASE,
)
UNRESOLVED_MARKER_RE = re.compile(r"(?<![A-Za-z0-9_])(?:TBD|待确认)(?![A-Za-z0-9_])", re.IGNORECASE)
COUPLING_HEADING_RE = re.compile(
    r"(?:关联系统与边界|关联系统|耦合分析|system coupling|related systems and boundaries)",
    re.IGNORECASE,
)
SELF_CHECK_HEADING_RE = re.compile(
    r"(?:验收口径|开发自查|程序自查|developer self[- ]check|implementation self[- ]check)",
    re.IGNORECASE,
)
CHECKBOX_RE = re.compile(r"^\s*[-*]\s+\[[ xX]\]\s+\S")


@dataclass
class Finding:
    rule: str
    severity: str
    line: int
    snippet: str
    message: str


def split_lines(md: str) -> list[str]:
    return md.replace("\r\n", "\n").replace("\r", "\n").split("\n")


def code_fence_mask(lines: list[str]) -> list[bool]:
    mask: list[bool] = []
    in_fence = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            mask.append(True)
            in_fence = not in_fence
        else:
            mask.append(in_fence)
    return mask


def plain_text(line: str) -> str:
    line = re.sub(r"`([^`]*)`", r"\1", line)
    line = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", line)
    line = re.sub(r"<[^>]+>", "", line)
    return line.replace("**", "").replace("__", "").replace("*", "").replace("_", "").strip()


def strip_tags(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text).strip()


def line_for_offset(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def heading_events(lines: list[str]) -> list[tuple[int, int, str, bool]]:
    out: list[tuple[int, int, str, bool]] = []
    resource_level: int | None = None
    for i, line in enumerate(lines):
        match = HEADING_RE.match(line)
        if not match:
            continue
        level = len(match.group(1))
        text = match.group(2).strip()
        if resource_level is not None and level <= resource_level:
            resource_level = None
        in_resource = resource_level is not None
        if RESOURCE_HEADING_RE.search(text):
            resource_level = level
            in_resource = True
        out.append((i, level, text, in_resource))
    return out


def rendered_heading_events(lines: list[str]) -> list[tuple[int, int, str, bool]]:
    """Heading events from rendered Markdown/HTML/XML exports.

    Publishing adapters often return HTML/XML in one long line. This accepts both
    closed headings (`<h3>Title</h3>`) and loose nested heading dumps, then reuses
    the same resource-list tracking as Markdown source mode.
    """
    full = "\n".join(lines)
    if "<h" not in full.lower():
        return heading_events(lines)

    raw: list[tuple[int, int, int, str]] = []
    seen_offsets: set[int] = set()

    for match in re.finditer(r"<h([1-6])(?:\s+[^>]*)?>(.*?)</h\1>", full, re.IGNORECASE | re.DOTALL):
        raw.append((
            match.start(),
            line_for_offset(full, match.start()),
            int(match.group(1)),
            strip_tags(match.group(2)),
        ))
        seen_offsets.add(match.start())

    block_tag = r"<(?:h[1-6]\b|p\b|ul\b|ol\b|table\b|checkbox\b|blockquote\b|hr\b|/h[1-6]\b|/section\b|section\b)"
    for match in re.finditer(r"<h([1-6])(?:\s+[^>]*)?>(.*?)(?=" + block_tag + r"|$)", full, re.IGNORECASE | re.DOTALL):
        if match.start() in seen_offsets:
            continue
        text_part = re.split(block_tag, match.group(2), maxsplit=1, flags=re.IGNORECASE)[0]
        raw.append((
            match.start(),
            line_for_offset(full, match.start()),
            int(match.group(1)),
            strip_tags(text_part),
        ))

    raw.sort(key=lambda item: item[0])
    out: list[tuple[int, int, str, bool]] = []
    resource_level: int | None = None
    for _offset, line_no, level, text in raw:
        if resource_level is not None and level <= resource_level:
            resource_level = None
        in_resource = resource_level is not None
        if RESOURCE_HEADING_RE.search(text):
            resource_level = level
            in_resource = True
        out.append((line_no - 1, level, text, in_resource))
    return out


def check_document_title(lines: list[str], rendered: bool) -> list[Finding]:
    full = "\n".join(lines)
    if rendered:
        title_match = re.search(r"<title(?:\s+[^>]*)?>(.*?)</title>", full, re.IGNORECASE | re.DOTALL)
        if title_match:
            if strip_tags(title_match.group(1)):
                return []
            return [Finding(
                "empty-title",
                "ERROR",
                line_for_offset(full, title_match.start()),
                title_match.group(0)[:120],
                "Rendered document has an empty title; make the first Markdown `# Title` or platform title non-empty.",
            )]
        events = rendered_heading_events(lines)
    else:
        events = heading_events(lines)

    if any(level == 1 and plain_text(text) for _i, level, text, _in_resource in events):
        return []
    return [Finding(
        "missing-title",
        "ERROR",
        1,
        "",
        "Design docs should start with a visible `# Title` so the reader and published document have a stable title.",
    )]


def check_role_marker_inline(lines: list[str]) -> list[Finding]:
    out: list[Finding] = []
    for i, _level, text, in_resource in heading_events(lines):
        if in_resource:
            continue
        if ROLE_RE.search(text):
            out.append(Finding(
                "role-marker-inline",
                "ERROR",
                i + 1,
                lines[i].strip(),
                "Role/color markers should not be mixed into feature headings; put them on a separate line or inside the resource list.",
            ))
    return out


def check_header_metadata(lines: list[str], mask: list[bool]) -> list[Finding]:
    out: list[Finding] = []
    seen_title = False
    before_second_heading = True
    for i, line in enumerate(lines):
        if mask[i]:
            continue
        if HEADING_RE.match(line):
            if seen_title:
                before_second_heading = False
            seen_title = True
        if before_second_heading and HEADER_META_RE.match(line) and not QUOTE_RE.match(line):
            out.append(Finding(
                "header-not-blockquote",
                "ERROR",
                i + 1,
                line.strip(),
                "Header metadata should be in a compact quote block, e.g. '> **Status:** Draft'.",
            ))
    return out


def check_facet_labels(lines: list[str], mask: list[bool]) -> list[Finding]:
    out: list[Finding] = []
    for i, line in enumerate(lines):
        if mask[i]:
            continue
        stripped = plain_text(line)
        if FACET_LABEL_SAMELINE_RE.search(line):
            out.append(Finding(
                "bold-facet-sameline",
                "ERROR",
                i + 1,
                line.strip(),
                "Planning facets are internal checks; do not expose them as bold same-line labels.",
            ))
        if HEADING_RE.match(line):
            heading_text = plain_text(HEADING_RE.match(line).group(2))
            if FACET_LABEL_EXACT_RE.match(heading_text):
                out.append(Finding(
                    "visible-facet-heading",
                    "WARN",
                    i + 1,
                    line.strip(),
                    "Use a concrete business heading instead of a visible planning facet.",
                ))
        elif FACET_LABEL_EXACT_RE.match(stripped):
            out.append(Finding(
                "visible-facet-label",
                "WARN",
                i + 1,
                line.strip(),
                "Use business wording instead of a standalone planning-facet label.",
            ))
    return out


def check_internal_anchors(lines: list[str], mask: list[bool]) -> list[Finding]:
    out: list[Finding] = []
    for i, line in enumerate(lines):
        if mask[i]:
            continue
        scrubbed = re.sub(r"`[^`]*`", "", line)
        for name, pattern in ANCHOR_PATTERNS:
            for match in pattern.finditer(scrubbed):
                out.append(Finding(
                    f"internal-anchor:{name}",
                    "ERROR",
                    i + 1,
                    match.group(0),
                    "Internal ids, local paths, or private anchors should not leak into reader-facing docs.",
                ))
    return out


def check_color(lines: list[str], mask: list[bool]) -> list[Finding]:
    out: list[Finding] = []
    for i, line in enumerate(lines):
        if not mask[i] and BANNED_COLOR_RE.search(line):
            out.append(Finding(
                "banned-color",
                "ERROR",
                i + 1,
                line.strip(),
                "Use a semantic color that the target platform supports; avoid grey/gray.",
            ))
    return out


def check_resource_headings(lines: list[str]) -> list[Finding]:
    out: list[Finding] = []
    seen: dict[str, int] = {}
    in_resource = False
    resource_level = 0
    current_function_line: int | None = None
    for i, line in enumerate(lines):
        match = HEADING_RE.match(line)
        if not match:
            continue
        level = len(match.group(1))
        text = plain_text(match.group(2))
        if in_resource and level <= resource_level:
            in_resource = False
            current_function_line = None
        if RESOURCE_HEADING_RE.search(text):
            in_resource = True
            resource_level = level
            seen = {}
            current_function_line = None
            continue
        if not in_resource:
            continue
        normalized = re.sub(rf"[{ROLE_MARKERS}\s/]+", "", text).lower()
        if level == resource_level + 1:
            if normalized in seen:
                out.append(Finding(
                    "duplicate-resource-function",
                    "ERROR",
                    i + 1,
                    line.strip(),
                    f"Resource-list function heading repeats line {seen[normalized]}; merge modules under one function heading.",
                ))
            else:
                seen[normalized] = i + 1
            current_function_line = i
        elif current_function_line is not None and level > resource_level + 1:
            if i > 0 and lines[i - 1].strip() == "":
                out.append(Finding(
                    "resource-module-leading-blank",
                    "WARN",
                    i + 1,
                    line.strip(),
                    "Inside one resource-list function, do not add a blank line before each module heading.",
                ))
    return out


def check_resource_missing_modules(lines: list[str], rendered: bool) -> list[Finding]:
    """Resource-list function headings should contain module headings before tasks."""
    out: list[Finding] = []
    events = rendered_heading_events(lines) if rendered else heading_events(lines)
    for idx, (line_idx, level, text, in_resource) in enumerate(events):
        if not in_resource or RESOURCE_HEADING_RE.search(text):
            continue
        prev_resource = None
        for j in range(idx - 1, -1, -1):
            if events[j][3] and RESOURCE_HEADING_RE.search(events[j][2]):
                prev_resource = events[j]
                break
        if prev_resource is None:
            continue
        resource_level = prev_resource[1]
        if level != resource_level + 1:
            continue

        end = len(events)
        for j in range(idx + 1, len(events)):
            next_line, next_level, _next_text, next_in_resource = events[j]
            if not next_in_resource or next_level <= level:
                end = j
                break
            _ = next_line
        has_module = any(events[j][1] > level for j in range(idx + 1, end))
        if not has_module:
            out.append(Finding(
                "resource-missing-module-heading",
                "ERROR",
                line_idx + 1,
                text,
                "Resource-list function headings should contain module headings before checklist items; avoid flattening all tasks directly under a function.",
            ))
    return out


def check_long_paragraphs(lines: list[str], mask: list[bool]) -> list[Finding]:
    out: list[Finding] = []
    for i, line in enumerate(lines):
        if mask[i]:
            continue
        stripped = line.strip()
        if not stripped or stripped.startswith(("#", "-", "*", ">", "|", "`")):
            continue
        visible = plain_text(stripped)
        sentence_count = len(re.findall(r"[。！？!?；;]", visible))
        if len(visible) >= 130 or sentence_count >= 4:
            out.append(Finding(
                "long-paragraph",
                "WARN",
                i + 1,
                stripped[:120],
                "Long paragraph detected; split into bullets, table, or diagram-backed points.",
            ))
    return out


def check_visuals(lines: list[str], mask: list[bool]) -> list[Finding]:
    out: list[Finding] = []
    for i, line in enumerate(lines):
        if mask[i] or not VISUAL_RE.search(line):
            continue
        window = lines[max(0, i - 3): min(len(lines), i + 4)]
        if not any(VISUAL_CAPTION_RE.search(item) for item in window):
            out.append(Finding(
                "missing-visual-caption",
                "WARN",
                i + 1,
                line.strip()[:120],
                "Visuals need a nearby caption explaining what the reader should look at.",
            ))
        for image in MARKDOWN_IMAGE_RE.finditer(line):
            alt = image.group(1).strip()
            if len(alt) > 36 or any(hint.lower() in alt.lower() for hint in LONG_ALT_HINTS):
                out.append(Finding(
                    "long-image-alt",
                    "WARN",
                    i + 1,
                    alt[:120],
                    "Image alt text should be short; put long descriptions in captions or the media manifest.",
                ))
    return out


def has_ux_source(md: str, lines: list[str]) -> bool:
    header = "\n".join(lines[:30]).lower()
    source_markers = (
        "ux / ui source", "ux source", "ui source", "ux design", "ui design",
        "figma", "prototype", "demo", "ux 设计案", "ui 设计案"
    )
    return any(marker in header for marker in source_markers) or any(
        marker in md.lower() for marker in ("figma.com", "prototype", "demo")
    )


def is_complete_spec(lines: list[str]) -> bool:
    header = "\n".join(lines[:30]).lower()
    return any(token in header for token in (
        "完整案", "complete spec", "final spec", "developer-facing", "implementation spec"
    ))


def check_complete_spec_ux_visual(lines: list[str], md: str) -> list[Finding]:
    if not is_complete_spec(lines) or not has_ux_source(md, lines):
        return []
    if re.search(r"(<img\b|!\[[^\]]*\]\([^)]+\))", md, re.IGNORECASE):
        return []
    allowed_handoff = (
        "media manifest", "media-manifest", "visual handoff", "image handoff",
        "screenshot handoff", "待补图", "无法取图", "permission", "unavailable",
        "needs-followup", "tbd"
    )
    if any(token in md.lower() for token in allowed_handoff):
        return []
    return [Finding(
        "complete-spec-no-ux-visual",
        "ERROR",
        1,
        "",
        "A complete spec with UX/UI/demo source should include real screenshots near the relevant rules, or a media handoff/manifest explaining the blocker.",
    )]


def check_complete_spec_low_fi(lines: list[str], mask: list[bool], md: str) -> list[Finding]:
    if not is_complete_spec(lines) or not LOW_FIDELITY_UI_RE.search(md):
        return []
    for i, line in enumerate(lines):
        if not mask[i] and LOW_FIDELITY_UI_RE.search(line):
            return [Finding(
                "complete-spec-low-fi-ui",
                "WARN",
                i + 1,
                line.strip()[:120],
                "Complete specs should use real UX/UI/demo evidence; keep low-fidelity UI sketches only with an explicit non-ui-diagram exception.",
            )]
    return []


def check_rendered_heading_numbers(lines: list[str], require_numbered_headings: bool) -> list[Finding]:
    if not require_numbered_headings:
        return []
    out: list[Finding] = []
    for line_idx, level, text, in_resource in rendered_heading_events(lines):
        if in_resource or level < 3 or not text:
            continue
        if not re.match(r"^\d+(?:\.\d+)*[.、]?\s+\S", text):
            out.append(Finding(
                "rendered-heading-missing-number",
                "ERROR",
                line_idx + 1,
                text,
                "Rendered h3/h4 feature headings are missing numbering; rerun the publishing adapter or fix the rendered outline.",
            ))
    return out


def check_nonhuman_terms(lines: list[str], mask: list[bool]) -> list[Finding]:
    out: list[Finding] = []
    for i, line in enumerate(lines):
        if mask[i]:
            continue
        for pattern, suggestion in NONHUMAN_TERMS.items():
            if re.search(pattern, line, re.IGNORECASE):
                out.append(Finding(
                    "nonhuman-term",
                    "WARN",
                    i + 1,
                    line.strip()[:120],
                    suggestion,
                ))
        for word in FILLER_WORDS:
            if word in line:
                out.append(Finding(
                    "filler-word",
                    "WARN",
                    i + 1,
                    line.strip()[:120],
                    "Remove filler phrasing unless it carries concrete information.",
                ))
    return out


def check_bold_headings(lines: list[str], mask: list[bool]) -> list[Finding]:
    out: list[Finding] = []
    for i, line in enumerate(lines):
        if mask[i]:
            continue
        match = HEADING_RE.match(line)
        if match and "**" in match.group(2):
            out.append(Finding(
                "bold-heading",
                "WARN",
                i + 1,
                line.strip(),
                "Headings already emphasize hierarchy; remove nested bold markup.",
            ))
    return out


def check_implementation_ready_contract(lines: list[str], mask: list[bool]) -> list[Finding]:
    out: list[Finding] = []
    headings = heading_events(lines)

    self_check_sections = [
        (index, line_idx, level)
        for index, (line_idx, level, text, _in_resource) in enumerate(headings)
        if SELF_CHECK_HEADING_RE.search(plain_text(text))
    ]
    if not self_check_sections:
        out.append(Finding(
            "implementation-ready-missing-self-check",
            "ERROR",
            1,
            "",
            "Implementation-ready requirements need a visible `验收口径` section with concise programmer self-check checkboxes.",
        ))
    else:
        for event_index, line_idx, level in self_check_sections:
            end_line = len(lines)
            for next_line_idx, next_level, _next_text, _in_resource in headings[event_index + 1:]:
                if next_level <= level:
                    end_line = next_line_idx
                    break
            checkbox_count = sum(
                1 for item in lines[line_idx + 1:end_line] if CHECKBOX_RE.match(item)
            )
            if checkbox_count == 0:
                out.append(Finding(
                    "implementation-ready-self-check-not-checklist",
                    "ERROR",
                    line_idx + 1,
                    lines[line_idx].strip(),
                    "`验收口径` should be a Markdown checkbox checklist for programmer self-check, not prose or a generic acceptance section.",
                ))

    for line_idx, _level, text, _in_resource in headings:
        normalized = plain_text(text)
        if UNRESOLVED_HEADING_RE.search(normalized):
            out.append(Finding(
                "implementation-ready-unresolved-heading",
                "ERROR",
                line_idx + 1,
                lines[line_idx].strip(),
                "Resolve requirement decisions before publishing; keep frozen decisions, TBDs, and open questions in conversation or handoff notes.",
            ))
        if COUPLING_HEADING_RE.search(normalized):
            out.append(Finding(
                "standalone-coupling-heading",
                "WARN",
                line_idx + 1,
                lines[line_idx].strip(),
                "Put cross-system effects and boundaries beside the functional rule they constrain; use a standalone coupling section only when the relationship itself is the feature.",
            ))

    for i, line in enumerate(lines):
        if mask[i]:
            continue
        scrubbed = re.sub(r"`[^`]*`", "", line)
        if UNRESOLVED_MARKER_RE.search(scrubbed):
            out.append(Finding(
                "implementation-ready-unresolved-marker",
                "ERROR",
                i + 1,
                line.strip()[:120],
                "Implementation-ready requirements contain conclusions only; resolve this marker or move the question to conversation / handoff.",
            ))
    return out


def run_checks(
    md: str,
    rendered: bool = False,
    require_numbered_headings: bool = False,
    implementation_ready: bool = False,
) -> list[Finding]:
    lines = split_lines(md)
    mask = code_fence_mask(lines)
    findings: list[Finding] = []
    findings.extend(check_document_title(lines, rendered))
    findings.extend(check_role_marker_inline(lines))
    findings.extend(check_header_metadata(lines, mask))
    findings.extend(check_facet_labels(lines, mask))
    findings.extend(check_internal_anchors(lines, mask))
    findings.extend(check_color(lines, mask))
    findings.extend(check_resource_headings(lines))
    findings.extend(check_resource_missing_modules(lines, rendered))
    findings.extend(check_long_paragraphs(lines, mask))
    findings.extend(check_visuals(lines, mask))
    findings.extend(check_complete_spec_ux_visual(lines, md))
    findings.extend(check_complete_spec_low_fi(lines, mask, md))
    if rendered:
        findings.extend(check_rendered_heading_numbers(lines, require_numbered_headings))
    findings.extend(check_nonhuman_terms(lines, mask))
    findings.extend(check_bold_headings(lines, mask))
    if implementation_ready:
        findings.extend(check_implementation_ready_contract(lines, mask))
    return sorted(findings, key=lambda f: (f.line, f.severity, f.rule))


def read_input(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("--strict", action="store_true", help="Treat WARN findings as failures.")
    parser.add_argument("--rendered", action="store_true", help="Validate an exported/published Markdown/HTML/XML artifact.")
    parser.add_argument(
        "--implementation-ready",
        action="store_true",
        help="Require resolved conclusions, a programmer self-check checklist, and inline cross-system boundaries.",
    )
    parser.add_argument(
        "--require-numbered-headings",
        action="store_true",
        help="In --rendered mode, require h3/h4 feature headings to have generated numeric prefixes.",
    )
    args = parser.parse_args(argv)

    findings = run_checks(
        read_input(args.path),
        rendered=args.rendered,
        require_numbered_headings=args.require_numbered_headings,
        implementation_ready=args.implementation_ready,
    )
    for f in findings:
        print(f"{f.severity} {f.rule} line {f.line}: {f.message}")
        print(f"  {f.snippet}")
    errors = [f for f in findings if f.severity == "ERROR"]
    warns = [f for f in findings if f.severity == "WARN"]
    if not findings:
        print("OK product-design-doc structure lint passed.")
    else:
        print(f"Summary: {len(errors)} ERROR, {len(warns)} WARN")
    return 1 if errors or (args.strict and warns) else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
