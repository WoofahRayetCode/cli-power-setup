#!/usr/bin/env python3
"""
Unit tests for data_vis_generator.py
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
import data_vis_generator as dvg


class TestDataVisGenerator(unittest.TestCase):

    def test_generate_interactive_timeline(self):
        events = [
            {"year": "1066", "title": "Battle of Hastings", "description": "Norman conquest of England."}
        ]
        html = dvg.generate_interactive_timeline(events, title="Norman Timeline")
        self.assertIn("Norman Timeline", html)
        self.assertIn("vis-timeline", html)
        self.assertIn("Battle of Hastings", html)

    def test_generate_network_graph(self):
        graph = {
            "nodes": [{"id": "zeus", "label": "Zeus"}, {"id": "hera", "label": "Hera"}],
            "links": [{"source": "zeus", "target": "hera"}]
        }
        html = dvg.generate_network_graph(graph, title="Greek Pantheon")
        self.assertIn("Greek Pantheon", html)
        self.assertIn("d3.v7.min.js", html)
        self.assertIn("zeus", html)


if __name__ == "__main__":
    unittest.main()
