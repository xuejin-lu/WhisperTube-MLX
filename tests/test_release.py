from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

from whispertube.release import (
    DEFAULT_MODEL,
    LOOPBACK_HOST,
    SMOKE_MODEL,
    HostFacts,
    approved_runtime_path,
    check_host,
    release_configuration,
)
from whispertube.version import __version__


class ReleaseConfigurationTests(unittest.TestCase):
    def test_version_matches_tracked_version_file(self):
        version_file = Path(__file__).parents[1] / "VERSION"
        self.assertEqual(__version__, version_file.read_text(encoding="utf-8").strip())

    def test_version_command_prints_only_the_project_version(self):
        completed = subprocess.run(
            [sys.executable, "-m", "whispertube.release", "--version"],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0)
        self.assertEqual(completed.stdout.strip(), __version__)
        self.assertEqual(completed.stderr, "")

    def test_supported_native_host_passes(self):
        report = check_host(
            HostFacts(
                system="Darwin",
                machine="arm64",
                macos_version="14.5",
                python_version=(3, 12),
                python_machine="arm64",
                ffmpeg_path="/opt/homebrew/bin/ffmpeg",
            )
        )
        self.assertTrue(report.ok)
        self.assertEqual(report.codes, ())

    def test_unsupported_host_reports_stable_actionable_codes(self):
        report = check_host(
            HostFacts(
                system="Darwin",
                machine="x86_64",
                macos_version="13.6",
                python_version=(3, 9),
                python_machine="x86_64",
                ffmpeg_path=None,
            )
        )
        self.assertFalse(report.ok)
        self.assertEqual(
            report.codes,
            ("HOST_ARCHITECTURE", "MACOS_VERSION", "PYTHON_VERSION", "PYTHON_ARCHITECTURE", "FFMPEG_MISSING"),
        )
        self.assertIn("Apple Silicon", report.message)
        self.assertIn("ffmpeg", report.message)

    def test_release_configuration_preserves_defaults_and_loopback(self):
        config = release_configuration(Path("/tmp/whispertube-release"))
        self.assertEqual(config.default_model, DEFAULT_MODEL)
        self.assertEqual(config.smoke_model, SMOKE_MODEL)
        self.assertEqual(config.loopback_host, LOOPBACK_HOST)
        self.assertEqual(config.venv_path, Path("/tmp/whispertube-release/.venv"))

    def test_approved_runtime_paths_reject_escape_and_absolute_user_paths(self):
        self.assertEqual(approved_runtime_path("temp/audio/run-1"), Path("temp/audio/run-1"))
        self.assertEqual(approved_runtime_path("outputs/transcripts"), Path("outputs/transcripts"))
        with self.assertRaises(ValueError):
            approved_runtime_path("temp/../../outside")
        with self.assertRaises(ValueError):
            approved_runtime_path("/Users/example/private")

    def test_release_scripts_delegate_without_public_share(self):
        root = Path(__file__).parents[1]
        setup = (root / "scripts/setup_macos.sh").read_text(encoding="utf-8")
        launch = (root / "scripts/launch_macos.sh").read_text(encoding="utf-8")
        self.assertIn("-m whispertube.release --check", setup)
        self.assertIn("-m whispertube.gui", launch)
        self.assertNotIn("--share", launch)
        self.assertNotIn("0.0.0.0", launch)


if __name__ == "__main__":
    unittest.main()
