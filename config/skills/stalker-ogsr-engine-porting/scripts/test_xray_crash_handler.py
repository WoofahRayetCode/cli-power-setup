#!/usr/bin/env python3
"""
Unit tests for xray_crash_handler.py
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.dirname(__file__))
import xray_crash_handler as xch


class TestXRayCrashHandler(unittest.TestCase):

    def test_resolve_wine_path(self):
        # Test Z:\ mapping
        with tempfile.NamedTemporaryFile(suffix=".log", delete=False) as f:
            temp_path = f.name
        try:
            # Simulate Wine Z:\ path
            wine_z = "Z:" + temp_path.replace("/", "\\")
            resolved = xch.resolve_wine_path(wine_z)
            self.assertIsNotNone(resolved)
            self.assertEqual(resolved.resolve(), Path(temp_path).resolve())
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def test_parse_xray_log(self):
        mock_log = """
[15.10.26 21:41:28.255] [324] Initializing File System...
[15.10.26 21:41:28.256] [324] * Detected CPU: AMD Ryzen 9 8940HX
[15.10.26 21:41:28.258] [324] [31121MB] physical memory installed
[15.10.26 21:41:28.258] [324] Engine memory usage (Working Set): [2567MB], peak: [2601MB]
[15.10.26 21:41:28.258] [324] ! [LUA ERROR] attempt to index global 'db' (a nil value)
[15.10.26 21:41:28.258] [324] FATAL ERROR
[15.10.26 21:41:28.258] [324] Expression    : fatal error
[15.10.26 21:41:28.258] [324] Function      : CScriptEngine::lua_error
[15.10.26 21:41:28.258] [324] File          : script_engine.cpp
[15.10.26 21:41:28.258] [324] Line          : 79
[15.10.26 21:41:28.258] [324] Description   : <no expression>
[15.10.26 21:41:28.258] [324] stack trace:
0x00007FF7B6011234 xrEngine.exe!CScriptEngine::lua_error()
0x00007FF7B6012456 xrEngine.exe!Level::Load()
"""
        with tempfile.NamedTemporaryFile("w+", suffix=".log", delete=False) as f:
            f.write(mock_log)
            temp_log_path = Path(f.name)

        try:
            report = xch.parse_xray_log(temp_log_path)
            self.assertTrue(report["fatal_error"])
            self.assertEqual(report["expression"], "fatal error")
            self.assertEqual(report["function"], "CScriptEngine::lua_error")
            self.assertEqual(report["file"], "script_engine.cpp")
            self.assertEqual(report["line"], "79")
            self.assertEqual(len(report["lua_errors"]), 1)
            self.assertIn("attempt to index global 'db'", report["lua_errors"][0])
            self.assertGreaterEqual(len(report["stack_trace"]), 1)
        finally:
            if temp_log_path.exists():
                temp_log_path.unlink()

    @patch("os.kill")
    def test_dismiss_process(self, mock_kill):
        # PID that does not exist in /proc
        mock_kill.return_value = None
        success = xch.dismiss_process(999999, timeout=0.1)
        self.assertTrue(success)
        mock_kill.assert_called()

    @patch("xray_crash_handler.scan_active_popups")
    @patch("xray_crash_handler.dismiss_process", return_value=True)
    def test_sweep_and_dismiss_mock(self, mock_dismiss, mock_scan):
        with tempfile.NamedTemporaryFile("w+", suffix=".log", delete=False) as f:
            f.write("FATAL ERROR\nExpression : memory out of bounds\n")
            log_path = Path(f.name)

        with tempfile.TemporaryDirectory() as temp_archive:
            mock_scan.return_value = [{
                "pid": 12345,
                "cmd": ["wine", "notepad.exe", str(log_path)],
                "is_notepad": True,
                "is_bugtrap": False,
                "log_path": log_path
            }]
            results = xch.sweep_and_dismiss(archive_dir=Path(temp_archive))
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0]["pid"], 12345)
            self.assertTrue(results[0]["dismissed"])
            self.assertEqual(results[0]["report"]["expression"], "memory out of bounds")

            # Verify report file written to archive
            archived = list(Path(temp_archive).glob("*.json"))
            self.assertEqual(len(archived), 1)

        if log_path.exists():
            log_path.unlink()


if __name__ == "__main__":
    unittest.main()
