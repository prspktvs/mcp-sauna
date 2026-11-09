#!/usr/bin/env python3
"""Check a generated mcp-sauna report against a reference-server fixture."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


SEVERITY = {"Low": 1, "Medium": 2, "High": 3, "Critical": 4}


def tool_matches(observed: str | None, expected: str) -> bool:
    """Match fixture tool names as exposed directly or through a host wrapper."""
    return observed == expected or (isinstance(observed, str) and observed.endswith(f"__{expected}"))


def load(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read {path}: {exc}") from exc
    if not isinstance(data, dict) or data.get("schema_version") != 1 or not isinstance(data.get("findings"), list):
        raise ValueError(f"{path} is not a mcp-sauna results.json v1 report")
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("variant", choices=("naive", "good"))
    parser.add_argument("results", type=Path)
    parser.add_argument("--expectations", type=Path, default=Path(__file__).resolve().parents[1] / "eval" / "reference-expectations.json")
    args = parser.parse_args()
    try:
        expectations = json.loads(args.expectations.read_text(encoding="utf-8"))[args.variant]
        report = load(args.results)
        findings = report["findings"]
    except (OSError, json.JSONDecodeError, KeyError, ValueError) as exc:
        print(f"reference eval: {exc}", file=sys.stderr)
        return 2

    observed = [item for item in findings if isinstance(item, dict)]
    problems: list[str] = []
    if args.variant == "naive":
        for rule_id, tool in expectations["required_findings"]:
            if not any(item.get("rule_id") == rule_id and tool_matches(item.get("tool"), tool) for item in observed):
                problems.append(f"missing seeded finding {rule_id} on {tool}")
        for rule_id, minimum in expectations["required_severity_at_least"].items():
            matching = [item for item in observed if item.get("rule_id") == rule_id]
            if not any(SEVERITY.get(item.get("severity"), 0) >= SEVERITY[minimum] for item in matching):
                problems.append(f"{rule_id} must be reported at {minimum} severity or higher")
        skipped_ids = {item.get("probe_id") for item in report.get("not_tested", []) if isinstance(item, dict)}
        if expectations.get("requires_identity_a_and_b") and "P4" in skipped_ids:
            problems.append("P4 identity isolation was skipped; S5 cannot count as established")
        environment = report.get("run_details", {}).get("environment")
        if environment not in {"dev", "test", "staging"}:
            problems.append("reference evaluation must use a non-production environment")
    else:
        forbidden = set(expectations["forbidden_severities"])
        for item in findings:
            if item.get("severity") in forbidden:
                problems.append(f"high-severity false-positive candidate {item.get('rule_id')} on {item.get('tool')}")

    result = "PASS" if not problems else "FAIL"
    print(f"{result}: {args.variant} reference-server evaluation ({len(findings)} findings)")
    for problem in problems:
        print(f"- {problem}")
    return 0 if not problems else 1


if __name__ == "__main__":
    raise SystemExit(main())
