from __future__ import annotations

import unittest
from pathlib import Path
import subprocess

from whispertube.release import inspect_artifacts


class ReleaseArtifactTests(unittest.TestCase):
    def test_public_release_docs_exist_and_defer_publication(self):
        root = Path(__file__).parents[1]
        troubleshooting = root / "docs/TROUBLESHOOTING.md"
        release = root / "docs/RELEASE.md"
        self.assertTrue(troubleshooting.is_file())
        self.assertTrue(release.is_file())
        release_text = release.read_text(encoding="utf-8")
        version = (root / "VERSION").read_text(encoding="utf-8").strip()
        self.assertIn(f"v{version}", release_text)
        self.assertIn("does not publish", release_text.lower())
        self.assertIn("GitHub Release", release_text)

    def test_troubleshooting_covers_required_privacy_sensitive_categories(self):
        text = (Path(__file__).parents[1] / "docs/TROUBLESHOOTING.md").read_text(encoding="utf-8").lower()
        for phrase in (
            "apple silicon",
            "rosetta",
            "ffmpeg",
            "model cache",
            "yt-dlp",
            "browser cookie",
            "keychain",
            "permission",
            "credentials",
        ):
            self.assertIn(phrase, text)

    def test_troubleshooting_documents_uninstall_boundaries(self):
        text = (Path(__file__).parents[1] / "docs/TROUBLESHOOTING.md").read_text(encoding="utf-8").lower()
        self.assertIn("uninstall", text)
        self.assertIn("model cache", text)
        self.assertIn("transcript", text)

    def test_artifact_inspection_returns_no_violations_for_tracked_files(self):
        root = Path(__file__).parents[1]
        tracked = subprocess.check_output(["git", "ls-files"], cwd=root, text=True).splitlines()
        self.assertEqual(inspect_artifacts(root, tracked), ())

    def test_tracked_files_do_not_include_runtime_private_artifacts(self):
        root = Path(__file__).parents[1]
        tracked = subprocess.check_output(
            ["git", "ls-files"], cwd=root, text=True
        ).splitlines()
        self.assertEqual(inspect_artifacts(root, tracked), ())


if __name__ == "__main__":
    unittest.main()
