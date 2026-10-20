#!/usr/bin/env python3
"""
Unit tests for lore_research_compiler.py
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
import lore_research_compiler as lrc


class TestLoreResearchCompiler(unittest.TestCase):

    def test_create_entity_dossier(self):
        dossier = lrc.create_entity_dossier(
            name="Odin Allfather",
            domain="Norse Mythology",
            culture_or_era="Viking Age Scandinavia",
            archetype="Wanderer / King / Sorcerer",
            summary="Chief god of the Aesir.",
            attributes=["Wisdom", "War", "Poetry", "Runes"],
            relationships=[{"type": "father_of", "target": "Thor"}]
        )
        self.assertEqual(dossier["id"], "odin_allfather")
        self.assertEqual(dossier["name"], "Odin Allfather")
        self.assertEqual(len(dossier["attributes"]), 4)
        self.assertEqual(dossier["relationships"][0]["target"], "Thor")

    def test_compile_timeline_bce_and_ce(self):
        raw_events = [
            {"year": "793 CE", "title": "Lindisfarne Raid"},
            {"year": "1200 BCE", "title": "Late Bronze Age Collapse"},
            {"year": "44 BCE", "title": "Assassination of Julius Caesar"},
            {"year": 1066, "title": "Battle of Hastings"}
        ]
        sorted_evs = lrc.compile_timeline(raw_events)
        titles = [e["title"] for e in sorted_evs]
        expected = [
            "Late Bronze Age Collapse",
            "Assassination of Julius Caesar",
            "Lindisfarne Raid",
            "Battle of Hastings"
        ]
        self.assertEqual(titles, expected)

    def test_build_relationship_graph(self):
        odin = lrc.create_entity_dossier("Odin", "Norse", "Viking", relationships=[{"type": "father_of", "target": "Thor"}])
        thor = lrc.create_entity_dossier("Thor", "Norse", "Viking", relationships=[{"type": "brother_of", "target": "Baldr"}])
        graph = lrc.build_relationship_graph([odin, thor])

        self.assertEqual(len(graph["nodes"]), 3)  # odin, thor, baldr
        self.assertEqual(len(graph["links"]), 2)

    def test_render_markdown_wiki_page(self):
        ent = lrc.create_entity_dossier("Anubis", "Egyptian", "Old Kingdom", summary="God of embalming and dead.")
        md = lrc.render_markdown_wiki_page(ent)
        self.assertIn("# Anubis", md)
        self.assertIn("Old Kingdom", md)


if __name__ == "__main__":
    unittest.main()
