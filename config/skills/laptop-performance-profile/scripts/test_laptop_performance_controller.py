#!/usr/bin/env python3
"""
Unit tests for laptop_performance_controller.py
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
import laptop_performance_controller as lpc


class TestLaptopPerformanceController(unittest.TestCase):

    def test_strip_ansi(self):
        text = "\x1b[31mRed text\x1b[0m and \x1b[1;32mGreen\x1b[0m"
        clean = lpc._strip_ansi(text)
        self.assertEqual(clean, "Red text and Green")

    @patch("laptop_performance_controller.is_omen_available", return_value=True)
    @patch("laptop_performance_controller._run")
    def test_set_power_profile_omen(self, mock_run, mock_omen):
        mock_run.return_value = (0, "Response: OK", "")
        # Test quiet alias
        self.assertTrue(lpc.set_power_profile("quiet"))
        mock_run.assert_called_with(["omen-cli", "power", "set-profile", "power-saver"])

        # Test performance
        self.assertTrue(lpc.set_power_profile("performance"))
        mock_run.assert_called_with(["omen-cli", "power", "set-profile", "performance"])

        # Test balanced
        self.assertTrue(lpc.set_power_profile("balanced"))
        mock_run.assert_called_with(["omen-cli", "power", "set-profile", "balanced"])

    @patch("laptop_performance_controller.is_omen_available", return_value=True)
    @patch("laptop_performance_controller._run")
    def test_set_fan_mode(self, mock_run, mock_omen):
        mock_run.return_value = (0, "Response: OK", "")
        self.assertTrue(lpc.set_fan_mode("auto"))
        mock_run.assert_called_with(["omen-cli", "fan", "set-mode", "auto"])

        self.assertTrue(lpc.set_fan_mode("max"))
        mock_run.assert_called_with(["omen-cli", "fan", "set-mode", "max"])

    @patch("laptop_performance_controller.get_current_profile", return_value="balanced")
    @patch("laptop_performance_controller.set_power_profile")
    def test_performance_context_revert(self, mock_set_profile, mock_get_profile):
        with lpc.PerformanceContext("performance"):
            mock_set_profile.assert_called_with("performance")
        mock_set_profile.assert_called_with("balanced")


if __name__ == "__main__":
    unittest.main()
