#!/usr/bin/env python3
"""Grade a sanitized mcp-sauna run log without network access."""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
from datetime import date
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit


RULES: dict[str, tuple[str, str, tuple[str, ...]]] = {
    "T1": ("Tool design", "Medium", ("static", "P1")),
    "T2": ("Tool design", "High", ("static", "P1")),
    "T3": ("Tool design", "Medium", ("static",)),
    "T4": ("Tool design", "High", ("static",)),
    "T5": ("Tool design", "Medium", ("static",)),
    "C1": ("Context cost", "Medium", ("static",)),
    "R1": ("Responses", "High", ("static", "P3")),
    "R2": ("Responses", "Medium", ("P1", "P3")),
    "R3": ("Responses", "Low", ("P1", "P3")),
    "E1": ("Errors", "High", ("P2",)),
    "E2": ("Errors", "High", ("P2",)),
    "S1": ("Safety", "Medium", ("static",)),
    "S2": ("Safety", "High", ("static",)),
    "S3": ("Safety", "High", ("static", "P5")),
    "S4": ("Safety", "Medium", ("static",)),
    "S5": ("Safety", "Critical", ("P4",)),
    "S6": ("Safety", "High", ("static", "P1", "P2", "P3", "P4", "P6")),
}
DIMENSIONS = ("Tool design", "Context cost", "Responses", "Errors", "Safety")
PROBE_DIMENSIONS = {
    "P1": ("Tool design", "Responses"),
    "P2": ("Errors",),
    "P3": ("Responses",),
    "P4": ("Safety",),
    "P5": ("Safety",),
    "P6": ("Safety",),
}
GRADE_ORDER = {"A": 0, "B": 1, "C": 2, "D": 3, "F": 4}
SEVERITY_ORDER = {"Critical": 4, "High": 3, "Medium": 2, "Low": 1}
CALL_KEYS = {
    "id", "phase", "task_id", "identity", "tool", "argument_fields", "result_fields",
    "result_items", "result_bytes", "estimated_tokens", "outcome", "error_class",
}


class InputError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise InputError(message)


def string(value: Any, label: str, *, nullable: bool = False) -> str | None:
    if nullable and value is None:
        return None
    require(isinstance(value, str) and bool(value.strip()), f"{label} must be a non-empty string")
    return value


def nonnegative_int(value: Any, label: str) -> int:
    require(isinstance(value, int) and not isinstance(value, bool) and value >= 0, f"{label} must be a non-negative integer")
    return value


def unique_strings(value: Any, label: str) -> list[str]:
    require(isinstance(value, list), f"{label} must be an array")
    values = [string(item, f"{label} item") for item in value]
    require(len(values) == len(set(values)), f"{label} must not contain duplicates")
    return values  # type: ignore[return-value]


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise InputError(f"cannot read JSON from {path}: {exc}") from exc
    require(isinstance(value, dict), f"{path} must contain a JSON object")
    return value


def validate_run(data: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    require(data.get("schema_version") == 1, "schema_version must be 1")
    require(set(data) == {"schema_version", "run", "tool_definitions", "tasks", "calls", "findings", "skipped_probes"}, "run.json has missing or unexpected top-level fields")

    run = data["run"]
    require(isinstance(run, dict), "run must be an object")
    require(set(run) == {"environment", "agent", "model", "date", "skill_version", "target_label"}, "run must contain exactly the documented fields")
    for key, value in run.items():
        string(value, f"run.{key}")
    try:
        parsed_date = date.fromisoformat(run["date"])
        require(parsed_date.isoformat() == run["date"], "run.date must use YYYY-MM-DD format")
    except ValueError as exc:
        raise InputError("run.date must use YYYY-MM-DD format") from exc
    require(run["environment"].casefold() in {"dev", "test", "staging"}, "run.environment must be dev, test, or staging")

    definitions = data["tool_definitions"]
    require(isinstance(definitions, list), "tool_definitions must be an array")
    tool_names: set[str] = set()
    for index, definition in enumerate(definitions):
        require(isinstance(definition, dict), f"tool_definitions[{index}] must be an object")
        require(set(definition) == {"name", "description", "input_schema", "output_schema", "annotations"}, f"tool_definitions[{index}] has missing or unexpected fields")
        name = string(definition["name"], f"tool_definitions[{index}].name")
        string(definition["description"], f"tool_definitions[{index}].description", nullable=True)
        require(definition["input_schema"] is None or isinstance(definition["input_schema"], dict), f"tool_definitions[{index}].input_schema must be an object or null")
        require(definition["output_schema"] is None or isinstance(definition["output_schema"], dict), f"tool_definitions[{index}].output_schema must be an object or null")
        require(definition["annotations"] is None or isinstance(definition["annotations"], dict), f"tool_definitions[{index}].annotations must be an object or null")
        require(name not in tool_names, f"duplicate tool name: {name}")
        tool_names.add(name)

    tasks = data["tasks"]
    require(isinstance(tasks, list), "tasks must be an array")
    task_ids: set[str] = set()
    for index, task in enumerate(tasks):
        require(isinstance(task, dict), f"tasks[{index}] must be an object")
        require(set(task) == {"id", "status", "attempts", "tool_calls", "estimated_tokens"}, f"tasks[{index}] has missing or unexpected fields")
        task_id = string(task["id"], f"tasks[{index}].id")
        require(task_id not in task_ids, f"duplicate task id: {task_id}")
        task_ids.add(task_id)
        require(task["status"] in {"success", "failed", "skipped"}, f"tasks[{index}].status must be success, failed, or skipped")
        attempts = nonnegative_int(task["attempts"], f"tasks[{index}].attempts")
        require((task["status"] == "skipped" and attempts == 0) or (task["status"] != "skipped" and attempts in {1, 2}), f"tasks[{index}] must have 0 attempts when skipped and 1 or 2 otherwise")
        nonnegative_int(task["tool_calls"], f"tasks[{index}].tool_calls")
        nonnegative_int(task["estimated_tokens"], f"tasks[{index}].estimated_tokens")
        require(task["status"] == "skipped" or task["tool_calls"] > 0, f"tasks[{index}] cannot be marked attempted without a tool call")

    calls = data["calls"]
    require(isinstance(calls, list), "calls must be an array")
    call_ids: set[str] = set()
    call_by_id: dict[str, dict[str, Any]] = {}
    for index, call in enumerate(calls):
        require(isinstance(call, dict), f"calls[{index}] must be an object")
        require(set(call) == CALL_KEYS, f"calls[{index}] has missing or unexpected fields; raw arguments/results are prohibited")
        call_id = string(call["id"], f"calls[{index}].id")
        require(call_id not in call_ids, f"duplicate call id: {call_id}")
        call_ids.add(call_id)
        call_by_id[call_id] = call
        require(call["phase"] in {"static", "P1", "P2", "P3", "P4", "P5", "P6"}, f"calls[{index}].phase is invalid")
        task_id = string(call["task_id"], f"calls[{index}].task_id", nullable=True)
        require(task_id is None or task_id in task_ids, f"calls[{index}] references unknown task {task_id}")
        require(call["identity"] in {None, "A", "B"}, f"calls[{index}].identity must be null, A, or B")
        tool = string(call["tool"], f"calls[{index}].tool")
        require(tool in tool_names, f"calls[{index}] references unknown tool {tool}")
        unique_strings(call["argument_fields"], f"calls[{index}].argument_fields")
        unique_strings(call["result_fields"], f"calls[{index}].result_fields")
        nonnegative_int(call["result_items"], f"calls[{index}].result_items")
        nonnegative_int(call["result_bytes"], f"calls[{index}].result_bytes")
        nonnegative_int(call["estimated_tokens"], f"calls[{index}].estimated_tokens")
        require(call["outcome"] in {"success", "error", "skipped"}, f"calls[{index}].outcome is invalid")
        string(call["error_class"], f"calls[{index}].error_class", nullable=True)
        require((call["outcome"] == "error") == (call["error_class"] is not None), f"calls[{index}] error_class must be present only for errors")

    findings = data["findings"]
    require(isinstance(findings, list), "findings must be an array")
    finding_ids: set[str] = set()
    seen_rule_tools: set[tuple[str, str | None]] = set()
    for index, finding in enumerate(findings):
        require(isinstance(finding, dict), f"findings[{index}] must be an object")
        require(set(finding) == {"id", "rule_id", "severity", "tool", "evidence_call_ids", "summary", "why_it_matters", "fix"}, f"findings[{index}] has missing or unexpected fields")
        finding_id = string(finding["id"], f"findings[{index}].id")
        require(finding_id not in finding_ids, f"duplicate finding id: {finding_id}")
        finding_ids.add(finding_id)
        rule_id = string(finding["rule_id"], f"findings[{index}].rule_id")
        require(rule_id in RULES, f"findings[{index}] uses unknown rule {rule_id}")
        _, expected_severity, allowed_phases = RULES[rule_id]
        require(finding["severity"] == expected_severity, f"findings[{index}] severity for {rule_id} must be {expected_severity}")
        tool = string(finding["tool"], f"findings[{index}].tool", nullable=True)
        require(tool is None or tool in tool_names or tool == "all tools", f"findings[{index}] references unknown tool {tool}")
        evidence_ids = unique_strings(finding["evidence_call_ids"], f"findings[{index}].evidence_call_ids")
        require(all(evidence_id in call_ids for evidence_id in evidence_ids), f"findings[{index}] references an unknown call")
        if "static" not in allowed_phases:
            require(bool(evidence_ids), f"behavioral finding {rule_id} needs a call reference")
        for evidence_id in evidence_ids:
            require(call_by_id[evidence_id]["phase"] in allowed_phases, f"{rule_id} cannot cite {call_by_id[evidence_id]['phase']} evidence")
        if rule_id == "S5":
            identities = {call_by_id[evidence_id]["identity"] for evidence_id in evidence_ids}
            require(identities == {"A", "B"}, "S5 needs cited calls from both identity A and identity B")
        for field in ("summary", "why_it_matters", "fix"):
            string(finding[field], f"findings[{index}].{field}")
        key = (rule_id, tool)
        require(key not in seen_rule_tools, f"duplicate finding for {rule_id} on {tool}")
        seen_rule_tools.add(key)

    skipped = data["skipped_probes"]
    require(isinstance(skipped, list), "skipped_probes must be an array")
    skipped_ids: set[str] = set()
    for index, probe in enumerate(skipped):
        require(isinstance(probe, dict), f"skipped_probes[{index}] must be an object")
        require(set(probe) == {"probe_id", "reason"}, f"skipped_probes[{index}] must contain probe_id and reason")
        probe_id = string(probe["probe_id"], f"skipped_probes[{index}].probe_id")
        require(probe_id in PROBE_DIMENSIONS, f"skipped_probes[{index}] has unknown probe {probe_id}")
        require(probe_id not in skipped_ids, f"duplicate skipped probe {probe_id}")
        skipped_ids.add(probe_id)
        string(probe["reason"], f"skipped_probes[{index}].reason")

    return run, definitions, tasks, calls, findings, skipped


def grade(severity: str) -> str:
    return {"Low": "B", "Medium": "C", "High": "D", "Critical": "F"}[severity]


def build_results(data: dict[str, Any]) -> dict[str, Any]:
    run, definitions, tasks, calls, findings, skipped = validate_run(data)
    dimension_findings: dict[str, list[dict[str, Any]]] = {dimension: [] for dimension in DIMENSIONS}
    for finding in findings:
        dimension = RULES[finding["rule_id"]][0]
        dimension_findings[dimension].append(finding)

    incomplete_reasons: dict[str, list[str]] = {dimension: [] for dimension in DIMENSIONS}
    for probe in skipped:
        for dimension in PROBE_DIMENSIONS[probe["probe_id"]]:
            incomplete_reasons[dimension].append(f"{probe['probe_id']} skipped: {probe['reason']}")

    dimensions: dict[str, dict[str, Any]] = {}
    known_grades: list[str] = []
    for dimension in DIMENSIONS:
        observed = dimension_findings[dimension]
        worst = max((grade(item["severity"]) for item in observed), key=lambda item: GRADE_ORDER[item], default="A")
        known_grades.append(worst)
        dimensions[dimension] = {
            "grade": worst,
            "status": "incomplete" if incomplete_reasons[dimension] else "complete",
            "finding_count": len(observed),
            "incomplete_reasons": incomplete_reasons[dimension],
        }

    any_incomplete = any(item["status"] == "incomplete" for item in dimensions.values())
    overall = "incomplete" if any_incomplete else max(known_grades, key=lambda item: GRADE_ORDER[item])
    ordered_findings = sorted(findings, key=lambda item: (-SEVERITY_ORDER[item["severity"]], item["rule_id"], item["tool"] or ""))
    top_fixes = []
    seen_fixes: set[str] = set()
    for finding in ordered_findings:
        if finding["fix"] not in seen_fixes:
            top_fixes.append({"rule_id": finding["rule_id"], "tool": finding["tool"], "fix": finding["fix"]})
            seen_fixes.add(finding["fix"])
        if len(top_fixes) == 3:
            break

    serialized_definitions = json.dumps(definitions, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    tool_definition_bytes = len(serialized_definitions)
    attempted_tasks = [task for task in tasks if task["status"] != "skipped"]
    successful_tasks = sum(1 for task in attempted_tasks if task["status"] == "success")
    metrics = {
        "task_count": len(tasks),
        "attempted_tasks": len(attempted_tasks),
        "skipped_tasks": len(tasks) - len(attempted_tasks),
        "successful_tasks": successful_tasks,
        "task_success_rate": (successful_tasks / len(attempted_tasks)) if attempted_tasks else None,
        "average_tool_calls_per_task": (sum(task["tool_calls"] for task in attempted_tasks) / len(attempted_tasks)) if attempted_tasks else None,
        "average_estimated_tokens_per_task": (sum(task["estimated_tokens"] for task in attempted_tasks) / len(attempted_tasks)) if attempted_tasks else None,
        "tool_definition_bytes": tool_definition_bytes,
        "estimated_tool_definition_tokens": math.ceil(tool_definition_bytes / 4),
        "unsafe_behaviors_found": sum(1 for finding in findings if finding["rule_id"].startswith("S")),
        "total_tool_calls": len(calls),
        "token_estimate_method": "Provider usage when available; otherwise ceil(UTF-8 bytes / 4). Estimates exclude assistant reasoning unless the host supplied usage.",
    }

    disclosures = [
        "Tool output passed through the model provider already used by the agent.",
        "This is an automated design review, not a security audit.",
    ]
    booking_url = os.environ.get("MCP_SAUNA_BOOKING_URL", "").strip()
    if booking_url:
        parsed_booking_url = urlsplit(booking_url)
        require(parsed_booking_url.scheme == "https" and bool(parsed_booking_url.netloc), "MCP_SAUNA_BOOKING_URL must be an https URL")
        disclosures.append(f"Book a full design review: {booking_url}")
    else:
        disclosures.append("Booking link not configured; publisher must set MCP_SAUNA_BOOKING_URL before public release.")

    return {
        "schema_version": 1,
        "skill_version": run["skill_version"],
        "summary": {
            "overall_grade": overall,
            "verdict": verdict(overall, ordered_findings),
            "top_fixes": top_fixes,
        },
        "scorecard": dimensions,
        "metrics": metrics,
        "findings": [
            {
                "id": item["id"],
                "rule_id": item["rule_id"],
                "severity": item["severity"],
                "tool": item["tool"],
                "evidence_call_ids": item["evidence_call_ids"],
                "summary": item["summary"],
                "why_it_matters": item["why_it_matters"],
                "fix": item["fix"],
            }
            for item in ordered_findings
        ],
        "not_tested": skipped,
        "run_details": run,
        "disclosures": disclosures,
    }


def verdict(overall: str, findings: list[dict[str, Any]]) -> str:
    if overall == "incomplete":
        return "The review is incomplete; skipped probes are not counted as passes."
    if overall == "F":
        return "Do not ship until the critical finding is resolved."
    if overall == "D":
        return "Fix the high-severity findings before production."
    if overall == "C":
        return "The server has design issues that should be fixed soon."
    if overall == "B":
        return "The review found only low-severity polish items."
    return "No design findings were established in the completed review."


def markdown_report(results: dict[str, Any]) -> str:
    summary = results["summary"]
    metrics = results["metrics"]
    lines = [
        "# mcp-sauna review report",
        "",
        f"**Overall grade: {summary['overall_grade']}** — {summary['verdict']}",
        "",
        "## Summary",
        "",
        "Top fixes:",
        "",
    ]
    if summary["top_fixes"]:
        for item in summary["top_fixes"]:
            target = f" ({item['tool']})" if item["tool"] else ""
            lines.append(f"- **{item['rule_id']}{target}:** {item['fix']}")
    else:
        lines.append("- No fixes were identified.")
    lines += ["", "## Scorecard", "", "| Dimension | Grade | Status | Findings |", "| --- | --- | --- | ---: |"]
    for dimension in DIMENSIONS:
        item = results["scorecard"][dimension]
        lines.append(f"| {dimension} | {item['grade']} | {item['status']} | {item['finding_count']} |")
    for dimension in DIMENSIONS:
        reasons = results["scorecard"][dimension]["incomplete_reasons"]
        for reason in reasons:
            lines.append(f"| | | Incomplete: {reason} | |")
    success_rate = metrics["task_success_rate"]
    success_text = "not measured" if success_rate is None else f"{metrics['successful_tasks']}/{metrics['attempted_tasks']} attempted ({success_rate:.0%}); {metrics['skipped_tasks']} skipped"
    avg_calls = "not measured" if metrics["average_tool_calls_per_task"] is None else f"{metrics['average_tool_calls_per_task']:.1f}"
    avg_tokens = "not measured" if metrics["average_estimated_tokens_per_task"] is None else f"{metrics['average_estimated_tokens_per_task']:.0f} (estimate)"
    lines += [
        "",
        "## Metrics",
        "",
        f"- Task success rate: {success_text}",
        f"- Average tool calls per task: {avg_calls}",
        f"- Average estimated tokens per task: {avg_tokens}",
        f"- Tool definitions: {metrics['estimated_tool_definition_tokens']} estimated tokens ({metrics['tool_definition_bytes']} UTF-8 bytes)",
        f"- Unsafe behaviors found: {metrics['unsafe_behaviors_found']}",
        f"- Total tool calls: {metrics['total_tool_calls']}",
        "",
        "## Findings",
        "",
    ]
    if results["findings"]:
        for item in results["findings"]:
            target = f" — {item['tool']}" if item["tool"] else ""
            evidence = f"; evidence: {', '.join(item['evidence_call_ids'])}" if item["evidence_call_ids"] else ""
            lines += [
                f"### {item['severity']}: {item['rule_id']}{target}",
                "",
                item["summary"],
                "",
                f"**Why it matters:** {item['why_it_matters']}{evidence}",
                "",
                f"**Fix:** {item['fix']}",
                "",
            ]
    else:
        lines += ["No findings were established.", ""]
    lines += ["## Not tested", ""]
    if results["not_tested"]:
        for item in results["not_tested"]:
            lines.append(f"- {item['probe_id']} skipped: {item['reason']}")
    else:
        lines.append("- None reported.")
    run = results["run_details"]
    lines += [
        "",
        "## Run details",
        "",
        f"- Environment: {run['environment']}",
        f"- Target: {run['target_label']}",
        f"- Agent/model: {run['agent']} / {run['model']}",
        f"- Date: {run['date']}",
        f"- Calls: {metrics['total_tool_calls']}",
        f"- Skill version: {run['skill_version']}",
        "",
        "Tool output passed through the model provider already used by the agent.",
        "",
        "This is an automated design review, not a security audit.",
    ]
    if len(results["disclosures"]) > 2 and results["disclosures"][2].startswith("Book a full design review:"):
        booking_url = results["disclosures"][2].split(": ", 1)[1]
        lines += ["", f"[Book a full design review]({booking_url})"]
    elif len(results["disclosures"]) > 2:
        lines += ["", results["disclosures"][2]]
    lines.append("")
    return "\n".join(lines)


def compare_results(left: dict[str, Any], right: dict[str, Any]) -> dict[str, Any]:
    left_high = {(item["rule_id"], item["tool"]) for item in left.get("findings", []) if item.get("severity") in {"High", "Critical"}}
    right_high = {(item["rule_id"], item["tool"]) for item in right.get("findings", []) if item.get("severity") in {"High", "Critical"}}
    left_grade = left.get("summary", {}).get("overall_grade")
    right_grade = right.get("summary", {}).get("overall_grade")
    same_grade = left_grade == right_grade
    same_high = left_high == right_high
    return {
        "stable": same_grade and same_high,
        "same_overall_grade": same_grade,
        "same_high_severity_findings": same_high,
        "first_grade": left_grade,
        "second_grade": right_grade,
        "first_only_high_findings": sorted([{"rule_id": rule_id, "tool": tool} for rule_id, tool in left_high - right_high], key=lambda x: (x["rule_id"], x["tool"] or "")),
        "second_only_high_findings": sorted([{"rule_id": rule_id, "tool": tool} for rule_id, tool in right_high - left_high], key=lambda x: (x["rule_id"], x["tool"] or "")),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_json", nargs="?", type=Path, help="sanitized run.json input")
    parser.add_argument("--json-out", type=Path, help="write results.json")
    parser.add_argument("--markdown-out", type=Path, help="write report.md")
    parser.add_argument("--compare", nargs=2, type=Path, metavar=("FIRST", "SECOND"), help="compare grade and High/Critical findings in two results.json files")
    args = parser.parse_args()

    try:
        if args.compare:
            result = compare_results(read_json(args.compare[0]), read_json(args.compare[1]))
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return 0 if result["stable"] else 1
        if args.run_json is None:
            parser.error("run_json is required unless --compare is used")
        results = build_results(read_json(args.run_json))
        encoded = json.dumps(results, indent=2, ensure_ascii=False) + "\n"
        report = markdown_report(results)
        if args.json_out:
            args.json_out.write_text(encoded, encoding="utf-8")
        if args.markdown_out:
            args.markdown_out.write_text(report, encoding="utf-8")
        if not args.json_out and not args.markdown_out:
            print(encoded, end="")
            print(report)
        return 0
    except InputError as exc:
        print(f"mcp-sauna: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
