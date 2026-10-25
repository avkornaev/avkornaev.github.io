import json
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

import sync_publications

from publication_data import build_items, dump_bibtex, merge_entries, parse_bibtex


ROOT = Path(__file__).resolve().parents[1]


class PublicationChecks(unittest.TestCase):
    def entry(self, key="local", **fields):
        return dict(entry_type="article", bibtex_key=key, title="A Study",
                    author="Kornaev, Alexei and Kornaeva, Elena", year="2026", **fields)

    def test_nested_braces_unicode_and_roundtrip(self):
        text = '@article{test, title={A {PINN} study}, author="Корнаев, Алексей", year=2026, month=Sept}'
        entries = parse_bibtex(text)
        self.assertEqual(parse_bibtex(dump_bibtex(entries)), entries)
        self.assertEqual(build_items(entries)[0]["authors"][0]["full"], "Алексей Корнаев")

    def test_macros_concatenation_and_truncated_entries_fail(self):
        for text in ('@string{venue="Test"}', '@article{x, title=unknown}',
                     '@article{x, title={A} # {B}}', '@article{x, title={A}'):
            with self.subTest(text=text), self.assertRaises(ValueError):
                parse_bibtex(text)

    def test_manual_corrections_survive_orcid_and_empty_fields_are_filled(self):
        local = self.entry(doi="10.1234/test", paper="https://example.org/paper")
        remote = dict(local, year="2025", author="Fallback Author", pages="1--8")
        merged = merge_entries([local], [remote])
        self.assertEqual(len(merged), 1)
        self.assertEqual(merged[0]["year"], "2026")
        self.assertEqual(merged[0]["author"], local["author"])
        self.assertEqual(merged[0]["pages"], "1--8")
        self.assertNotIn("pages", local)

    def test_same_title_with_different_year_is_not_added_twice(self):
        local = self.entry()
        remote = dict(local, bibtex_key="remote", year="2025", title="A study!")
        self.assertEqual(len(merge_entries([local], [remote])), 1)

    def test_distinct_works_with_colliding_keys_are_both_preserved(self):
        local = self.entry()
        remote = dict(local, title="Different study")
        merged = merge_entries([local], [remote])
        self.assertEqual(len(build_items(merged)), 2)
        self.assertNotEqual(merged[0]["bibtex_key"], merged[1]["bibtex_key"])

    def test_duplicate_keys_titles_and_dois_are_rejected(self):
        local = self.entry(doi="10.1234/test")
        candidates = [dict(local, title="Other"), dict(local, bibtex_key="other"),
                      dict(local, bibtex_key="other", title="Other", doi="https://doi.org/10.1234/TEST")]
        for candidate in candidates:
            with self.subTest(candidate=candidate), self.assertRaises(ValueError):
                build_items([local, candidate])

    def test_sync_never_invents_single_author_when_metadata_is_missing(self):
        payload = {"group": [{"work-summary": [{
            "title": {"title": {"value": "Paper with missing contributor data"}},
            "publication-date": {"year": {"value": "2026"}},
            "type": "journal-article"}]}]}
        with patch.object(sync_publications, "fetch_json", return_value=payload), \
                patch.object(sync_publications, "load_overrides", return_value={}), \
                patch("sys.stderr"):
            self.assertEqual(sync_publications.fetch_orcid_items(), [])

    def test_repository_data_matches_bibliography_and_has_no_shadow_dataset(self):
        entries = parse_bibtex((ROOT / "bibliography/publications.bib").read_text())
        data = json.loads((ROOT / "_data/publications.json").read_text())
        self.assertEqual(data["items"], build_items(entries))
        self.assertFalse((ROOT / "_data/publications.yml").exists())
        self.assertGreaterEqual(len(entries), 84)
        self.assertTrue(all(item["authors"] for item in data["items"]))
        self.assertFalse(any("TODO-check" in item["title"] for item in data["items"]))

    def test_offline_rebuild_is_deterministic_and_preserves_bibtex(self):
        paths = [ROOT / path for path in ("bibliography/publications.bib",
                 "_data/publications.json", "generated/publications.md")]
        before = [path.read_bytes() for path in paths]
        subprocess.run([sys.executable, str(ROOT / "scripts/sync_publications.py"), "--offline"],
                       check=True, capture_output=True)
        self.assertEqual(before, [path.read_bytes() for path in paths])


if __name__ == "__main__":
    unittest.main()
