#!/usr/bin/env python3
"""
Unit tests for task_velocity_guard.py
"""

import unittest
import tempfile
import sys
import os
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(__file__))
import task_velocity_guard as tvg


class TestTaskVelocityGuard(unittest.TestCase):

    def setUp(self):
        self.tmp_ledger = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self.tmp_ledger.close()
        tvg.LEDGER_PATH = Path(self.tmp_ledger.name)

    def tearDown(self):
        if tvg.LEDGER_PATH.exists():
            tvg.LEDGER_PATH.unlink()

    def test_start_and_record_step(self):
        tvg.start_task("test_feature", step_budget=3, max_minutes=5)
        res = tvg.record_step("Created file a.py", target_file="a.py")
        self.assertEqual(res["step"], 1)
        self.assertEqual(res["status"], "HEALTHY")

    def test_step_budget_alert(self):
        tvg.start_task("test_budget", step_budget=2, max_minutes=10)
        tvg.record_step("Step 1")
        tvg.record_step("Step 2")
        res3 = tvg.record_step("Step 3")
        self.assertEqual(res3["status"], "AT_RISK")
        self.assertTrue(any("STEP BUDGET EXCEEDED" in a for a in res3["alerts"]))

    def test_churn_loop_breaker(self):
        tvg.start_task("test_churn", step_budget=10, max_minutes=10)
        tvg.record_step("Edit 1", target_file="main.py")
        tvg.record_step("Edit 2", target_file="main.py")
        res3 = tvg.record_step("Edit 3", target_file="main.py")
        self.assertEqual(res3["status"], "AT_RISK")
        self.assertTrue(any("CHURN LOOP DETECTED" in a for a in res3["alerts"]))


if __name__ == "__main__":
    unittest.main()
