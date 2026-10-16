#!/usr/bin/env python3
"""
Unit tests for static_site_scaffolder.py
"""

import unittest
import tempfile
import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))
import static_site_scaffolder as sss


class TestStaticSiteScaffolder(unittest.TestCase):

    def test_scaffold_pure_static(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            dest = Path(tmp_dir) / "test_site"
            sss.scaffold_pure_static(dest, "Mythology Portal")

            self.assertTrue((dest / "index.html").exists())
            self.assertTrue((dest / ".github/workflows/deploy.yml").exists())

            index_content = (dest / "index.html").read_text(encoding="utf-8")
            self.assertIn("Mythology Portal", index_content)
            self.assertIn("Historical Chronicles", index_content)

            wf_content = (dest / ".github/workflows/deploy.yml").read_text(encoding="utf-8")
            self.assertIn("deploy-pages", wf_content)


if __name__ == "__main__":
    unittest.main()
