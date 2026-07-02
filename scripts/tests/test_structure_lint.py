#!/usr/bin/env python3
"""Golden checks for product-design-doc structure_lint.

Run from the skill root:
    python3 scripts/tests/test_structure_lint.py
"""
from __future__ import annotations

import os
import subprocess
import sys

SCRIPT_DIR = os.path.dirname(__file__)
SCRIPT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "structure_lint.py"))
sys.path.insert(0, os.path.dirname(SCRIPT))

import structure_lint as sl  # noqa: E402


GOOD_DOC = """# Merchant Trading Spec

> **Type:** Feature iteration
> **Status:** Draft
> **UX / UI Source:** [Figma](https://example.com) (interface authority)
> **Version / Scope:** v1

## Core Experience

The merchant lets players exchange currency and materials for goods. The first version keeps pricing explicit and only confirms the transaction after the player reviews the cost.

> **Screenshot:** Merchant detail panel. Focus on item information, cost preview, quantity controls, and the confirm action.

![Merchant panel](merchant-panel.png)

## Feature Details

### Trading Entry

Players open the merchant from the main hub and select an item from the shelf.

#### Cost Preview

- **Currency purchase:** Only spends currency.
- **Material exchange:** Only consumes the listed materials.
- **Mixed cost:** Consumes both currency and materials.

## Delivery / Handoff

### Resource List

#### Engineering
##### Purchase Flow
- [ ] Validate price, stock, and inventory space <text color="red">P0</text>

#### UX / UI
##### Merchant Panel
- [ ] Default, insufficient funds, and success states <text color="red">P0</text>
"""


def expect_rule(doc: str, rule: str, severity: str = "ERROR", **kwargs: object) -> bool:
    return any(f.rule == rule and f.severity == severity for f in sl.run_checks(doc, **kwargs))


def main() -> int:
    failed = 0

    good_errors = [f for f in sl.run_checks(GOOD_DOC) if f.severity == "ERROR"]
    if good_errors:
        failed += 1
        print("FAIL good-doc: expected zero ERROR")
        for finding in good_errors:
            print(f"  {finding.rule}: {finding.message}")
    else:
        print("ok   good-doc")

    missing_title = """> **Type:** Feature iteration

## Core Experience

Text.
"""
    if not expect_rule(missing_title, "missing-title"):
        failed += 1
        print("FAIL missing-title")
    else:
        print("ok   missing-title")

    no_ux_visual = """# Merchant Trading Spec

> **Type:** Complete spec
> **UX / UI Source:** [Figma](https://example.com)

## Core Experience

Only a link, no screenshot or media handoff.
"""
    if not expect_rule(no_ux_visual, "complete-spec-no-ux-visual"):
        failed += 1
        print("FAIL complete-spec-no-ux-visual")
    else:
        print("ok   complete-spec-no-ux-visual")

    resource_flat = """# Delivery Spec

## Delivery / Handoff

### Resource List

#### Engineering
- [ ] Implement validation
"""
    if not expect_rule(resource_flat, "resource-missing-module-heading"):
        failed += 1
        print("FAIL resource-missing-module-heading")
    else:
        print("ok   resource-missing-module-heading")

    rendered_good = """<title>Merchant Trading Spec</title><h2>Feature Details</h2><h3>1. Trading Entry</h3><p>Text.</p><h4>1.1. Cost Preview</h4><ul><li>Text.</li></ul><h2>Delivery / Handoff</h2><h3>Resource List</h3><h4>Engineering</h4><h5>Purchase Flow</h5><checkbox done="false">Validate price</checkbox>"""
    rendered_bad = """<title></title><h2>Feature Details</h2><h3>Trading Entry</h3><p>Text.</p><h4>Cost Preview</h4><ul><li>Text.</li></ul><h2>Delivery / Handoff</h2><h3>Resource List</h3><h4>Engineering</h4><checkbox done="false">Validate price</checkbox>"""
    rendered_good_errors = [
        f for f in sl.run_checks(rendered_good, rendered=True, require_numbered_headings=True)
        if f.severity == "ERROR"
    ]
    rendered_bad_rules = {
        f.rule
        for f in sl.run_checks(rendered_bad, rendered=True, require_numbered_headings=True)
        if f.severity == "ERROR"
    }
    expected_rendered = {"empty-title", "rendered-heading-missing-number", "resource-missing-module-heading"}
    if rendered_good_errors:
        failed += 1
        print("FAIL rendered-good")
        for finding in rendered_good_errors:
            print(f"  {finding.rule}: {finding.message}")
    elif not expected_rendered.issubset(rendered_bad_rules):
        failed += 1
        print(f"FAIL rendered-bad: got {rendered_bad_rules}")
    else:
        print("ok   rendered-gate")

    rc_bad = subprocess.run(
        [sys.executable, SCRIPT, "-"],
        input=no_ux_visual,
        text=True,
        capture_output=True,
        check=False,
    ).returncode
    rc_rendered_bad = subprocess.run(
        [sys.executable, SCRIPT, "--rendered", "--require-numbered-headings", "-"],
        input=rendered_bad,
        text=True,
        capture_output=True,
        check=False,
    ).returncode
    if rc_bad != 1 or rc_rendered_bad != 1:
        failed += 1
        print(f"FAIL cli-exit-codes: bad={rc_bad}, rendered_bad={rc_rendered_bad}")
    else:
        print("ok   cli-exit-codes")

    print(f"\n{'ALL PASS' if failed == 0 else str(failed) + ' FAILED'}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
