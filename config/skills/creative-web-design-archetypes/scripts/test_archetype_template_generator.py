#!/usr/bin/env python3
"""
Unit tests for archetype_template_generator.py
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
import archetype_template_generator as atg


class TestArchetypeTemplateGenerator(unittest.TestCase):

    def test_generate_mythic_parchment(self):
        html = atg.generate_template("mythic-parchment", "Norse Eddas", "In the beginning was Ymir.")
        self.assertIn("Norse Eddas", html)
        self.assertIn("Cinzel", html)
        self.assertIn("--parchment-bg", html)

    def test_generate_neo_brutalism(self):
        html = atg.generate_template("neo-brutalism", "Hacker Hub", "Raw CSS grids.")
        self.assertIn("Hacker Hub", html)
        self.assertIn("Cabinet Grotesk", html)
        self.assertIn("5px 5px 0px var(--black)", html)

    def test_generate_cyberpunk_terminal(self):
        html = atg.generate_template("cyberpunk-terminal", "Mainframe", "Access granted.")
        self.assertIn("Mainframe", html)
        self.assertIn("Orbitron", html)
        self.assertIn("scanlines", html.lower())

    def test_generate_dark_glassmorphism(self):
        html = atg.generate_template("dark-glassmorphism", "Aether UI", "Frosted glass container.")
        self.assertIn("Aether UI", html)
        self.assertIn("backdrop-filter: blur(20px)", html)


if __name__ == "__main__":
    unittest.main()
