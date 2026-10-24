#!/usr/bin/env python3
"""
Unit tests for verification_reasoner.py
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
import verification_reasoner as vr


class TestVerificationReasoner(unittest.TestCase):

    def test_generate_cove_framework(self):
        res = vr.generate_cove_framework("Switching to D3.js will improve graph render performance")
        self.assertEqual(len(res["verification_queries"]), 5)
        self.assertIn("Invariant Check", res["verification_queries"][0])
        self.assertIn("Pre-Mortem Red Team", res["verification_queries"][1])

    def test_rank_hypotheses_ockham(self):
        hypotheses = [
            {"name": "Complex compiler bug", "probability": 2, "verification_effort": 8, "complexity": 9},  # score: 2 / 72 = 0.028
            {"name": "Missing file in assets", "probability": 8, "verification_effort": 1, "complexity": 1},   # score: 8 / 1 = 8.0
            {"name": "Bad environment variable", "probability": 6, "verification_effort": 2, "complexity": 2} # score: 6 / 4 = 1.5
        ]
        ranked = vr.rank_hypotheses_ockham(hypotheses)
        self.assertEqual(ranked[0]["name"], "Missing file in assets")
        self.assertEqual(ranked[1]["name"], "Bad environment variable")
        self.assertEqual(ranked[2]["name"], "Complex compiler bug")


if __name__ == "__main__":
    unittest.main()
