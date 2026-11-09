import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTATIONS = json.loads((ROOT / "eval" / "reference-expectations.json").read_text(encoding="utf-8"))
SEVERITIES = {
    "T1": "Medium", "T2": "High", "T3": "Medium", "T4": "High", "T5": "Medium",
    "C1": "Medium", "R1": "High", "R2": "Medium", "R3": "Low", "E1": "High",
    "E2": "High", "S1": "Medium", "S2": "High", "S3": "High", "S4": "Medium",
    "S5": "Critical", "S6": "High",
}


class ReferenceEvalCheckerTests(unittest.TestCase):
    def check(self, variant, findings):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "results.json"
            path.write_text(json.dumps({"schema_version": 1, "findings": findings, "not_tested": [], "run_details": {"environment": "test"}}), encoding="utf-8")
            return subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "check_reference_eval.py"), variant, str(path)],
                capture_output=True, text=True, check=False,
            )

    def test_naive_passes_when_all_seeded_rule_tool_pairs_are_present(self):
        findings = [
            {"rule_id": rule_id, "tool": tool, "severity": SEVERITIES[rule_id]}
            for rule_id, tool in EXPECTATIONS["naive"]["required_findings"]
        ]
        result = self.check("naive", findings)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_naive_fails_when_a_seeded_finding_is_missing(self):
        findings = [
            {"rule_id": rule_id, "tool": tool, "severity": SEVERITIES[rule_id]}
            for rule_id, tool in EXPECTATIONS["naive"]["required_findings"][1:]
        ]
        result = self.check("naive", findings)
        self.assertEqual(result.returncode, 1)
        self.assertIn("missing seeded finding", result.stdout)

    def test_naive_cannot_claim_identity_isolation_when_p4_was_skipped(self):
        findings = [
            {"rule_id": rule_id, "tool": tool, "severity": SEVERITIES[rule_id]}
            for rule_id, tool in EXPECTATIONS["naive"]["required_findings"]
        ]
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "results.json"
            path.write_text(json.dumps({
                "schema_version": 1, "findings": findings,
                "not_tested": [{"probe_id": "P4", "reason": "No second identity"}],
                "run_details": {"environment": "test"},
            }), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "check_reference_eval.py"), "naive", str(path)],
                capture_output=True, text=True, check=False,
            )
        self.assertEqual(result.returncode, 1)
        self.assertIn("P4 identity isolation was skipped", result.stdout)

    def test_good_fails_for_high_severity_finding(self):
        result = self.check("good", [{"rule_id": "T2", "tool": "search_orders", "severity": "High"}])
        self.assertEqual(result.returncode, 1)
        self.assertIn("false-positive candidate", result.stdout)


if __name__ == "__main__":
    unittest.main()
