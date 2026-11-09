import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("sauna_grade", ROOT / "scripts" / "grade.py")
grade = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(grade)


def run_data():
    return {
        "schema_version": 1,
        "run": {
            "environment": "test", "agent": "Codex", "model": "test-model",
            "date": "2026-11-09", "skill_version": "0.1.0", "target_label": "fake server",
        },
        "tool_definitions": [{
            "name": "search_orders", "description": "Search orders by readable fields.",
            "input_schema": {"type": "object", "properties": {}, "required": []},
            "output_schema": None, "annotations": {"readOnlyHint": True},
        }],
        "tasks": [{"id": "TASK-01", "success": True, "attempts": 1, "tool_calls": 1, "estimated_tokens": 20}],
        "calls": [{
            "id": "CALL-01", "phase": "P1", "task_id": "TASK-01", "identity": None, "tool": "search_orders",
            "argument_fields": ["query"], "result_fields": ["orders"], "result_items": 1,
            "result_bytes": 80, "estimated_tokens": 20, "outcome": "success", "error_class": None,
        }],
        "findings": [],
        "skipped_probes": [],
    }


class GradeTests(unittest.TestCase):
    def test_complete_clean_run_gets_a(self):
        result = grade.build_results(run_data())
        self.assertEqual(result["summary"]["overall_grade"], "A")
        self.assertEqual(result["scorecard"]["Responses"]["status"], "complete")
        self.assertEqual(result["metrics"]["estimated_tool_definition_tokens"], (result["metrics"]["tool_definition_bytes"] + 3) // 4)

    def test_skipped_probe_makes_dimension_and_overall_incomplete(self):
        data = run_data()
        data["skipped_probes"] = [{"probe_id": "P4", "reason": "No second test identity."}]
        result = grade.build_results(data)
        self.assertEqual(result["summary"]["overall_grade"], "incomplete")
        self.assertEqual(result["scorecard"]["Safety"]["status"], "incomplete")

    def test_grade_uses_fixed_rule_severity_and_evidence(self):
        data = run_data()
        data["findings"] = [{
            "id": "F-1", "rule_id": "R2", "severity": "Medium", "tool": "search_orders",
            "evidence_call_ids": ["CALL-01"], "summary": "Extra unrelated fields were returned.",
            "why_it_matters": "They increase the result size.", "fix": "Return only task-relevant fields.",
        }]
        result = grade.build_results(data)
        self.assertEqual(result["scorecard"]["Responses"]["grade"], "C")
        data["findings"][0]["severity"] = "Low"
        with self.assertRaises(grade.InputError):
            grade.build_results(data)

    def test_call_log_rejects_raw_values(self):
        data = run_data()
        data["calls"][0]["result"] = {"customer": "sensitive value"}
        with self.assertRaisesRegex(grade.InputError, "raw arguments/results are prohibited"):
            grade.build_results(data)

    def test_behavioral_finding_requires_call_evidence(self):
        data = run_data()
        data["findings"] = [{
            "id": "F-1", "rule_id": "E1", "severity": "High", "tool": "search_orders",
            "evidence_call_ids": [], "summary": "The error is not actionable.",
            "why_it_matters": "The user cannot recover.", "fix": "Return a safe next step.",
        }]
        with self.assertRaises(grade.InputError):
            grade.build_results(data)

    def test_identity_finding_needs_both_test_connections(self):
        data = run_data()
        data["calls"] = [
            {"id": "CALL-A", "phase": "P4", "task_id": None, "identity": "A", "tool": "search_orders", "argument_fields": ["query"], "result_fields": ["orders"], "result_items": 1, "result_bytes": 80, "estimated_tokens": 20, "outcome": "success", "error_class": None},
            {"id": "CALL-B", "phase": "P4", "task_id": None, "identity": "B", "tool": "search_orders", "argument_fields": ["query"], "result_fields": ["orders"], "result_items": 1, "result_bytes": 80, "estimated_tokens": 20, "outcome": "success", "error_class": None},
        ]
        data["findings"] = [{
            "id": "F-1", "rule_id": "S5", "severity": "Critical", "tool": "search_orders",
            "evidence_call_ids": ["CALL-A", "CALL-B"], "summary": "Both identities received the restricted test record.",
            "why_it_matters": "Access boundaries are not maintained.", "fix": "Enforce authorization for each authenticated identity.",
        }]
        self.assertEqual(grade.build_results(data)["scorecard"]["Safety"]["grade"], "F")
        data["findings"][0]["evidence_call_ids"] = ["CALL-A"]
        with self.assertRaises(grade.InputError):
            grade.build_results(data)

    def test_repeatability_compares_overall_grade_and_high_findings(self):
        first = {"summary": {"overall_grade": "D"}, "findings": [{"rule_id": "E1", "tool": "search_orders", "severity": "High"}]}
        same = {"summary": {"overall_grade": "D"}, "findings": [{"rule_id": "E1", "tool": "search_orders", "severity": "High", "summary": "Different wording"}]}
        changed = {"summary": {"overall_grade": "C"}, "findings": []}
        self.assertTrue(grade.compare_results(first, same)["stable"])
        self.assertFalse(grade.compare_results(first, changed)["stable"])

    def test_cli_writes_machine_and_markdown_reports_and_compares(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            run_path = root / "run.json"
            run_path.write_text(json.dumps(run_data()), encoding="utf-8")
            json_path = root / "results.json"
            markdown_path = root / "report.md"
            command = [sys.executable, str(ROOT / "scripts" / "grade.py"), str(run_path), "--json-out", str(json_path), "--markdown-out", str(markdown_path)]
            first = subprocess.run(command, capture_output=True, text=True, check=False)
            second = subprocess.run(command, capture_output=True, text=True, check=False)
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
            self.assertEqual(second.returncode, 0, second.stdout + second.stderr)
            results = json.loads(json_path.read_text(encoding="utf-8"))
            report = markdown_path.read_text(encoding="utf-8")
            self.assertEqual(results["summary"]["overall_grade"], "A")
            self.assertIn("not a security audit", report)
            comparison = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "grade.py"), "--compare", str(json_path), str(json_path)],
                capture_output=True, text=True, check=False,
            )
            self.assertEqual(comparison.returncode, 0, comparison.stdout + comparison.stderr)

    def test_booking_link_requires_https_and_is_included_when_configured(self):
        with patch.dict("os.environ", {"MCP_SAUNA_BOOKING_URL": "https://example.org/review"}):
            result = grade.build_results(run_data())
            report = grade.markdown_report(result)
            self.assertIn("https://example.org/review", result["disclosures"][2])
            self.assertIn("[Book a full design review](https://example.org/review)", report)
        with patch.dict("os.environ", {"MCP_SAUNA_BOOKING_URL": "javascript:alert(1)"}):
            with self.assertRaises(grade.InputError):
                grade.build_results(run_data())


if __name__ == "__main__":
    unittest.main()
