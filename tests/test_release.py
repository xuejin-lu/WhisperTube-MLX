from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
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


class ReleaseScriptTests(unittest.TestCase):
    def _copy_script(self, root: Path, name: str) -> Path:
        destination = root / "scripts" / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        source = Path(__file__).parents[1] / "scripts" / name
        shutil.copy2(source, destination)
        destination.chmod(0o755)
        return destination

    def _write_executable(self, path: Path, content: str) -> Path:
        path.write_text(content, encoding="utf-8")
        path.chmod(0o755)
        return path

    def test_launch_uses_project_yt_dlp_with_clean_path_and_preserves_arguments(self):
        with tempfile.TemporaryDirectory(prefix="whispertube release ") as directory:
            root = Path(directory)
            launcher = self._copy_script(root, "launch_macos.sh")
            bin_dir = root / ".venv" / "bin"
            bin_dir.mkdir(parents=True)
            capture = root / "capture"
            fake_python = self._write_executable(
                bin_dir / "python",
                """#!/bin/sh
set -eu
printf '%s\\n' \"$PATH\" > \"$CAPTURE_FILE.path\"
printf '%s\\n' \"$*\" > \"$CAPTURE_FILE.args\"
command -v yt-dlp > \"$CAPTURE_FILE.yt_dlp\"
""",
            )
            self._write_executable(bin_dir / "yt-dlp", "#!/bin/sh\nexit 0\n")
            environment = os.environ.copy()
            environment.update({"PATH": "/usr/bin:/bin", "CAPTURE_FILE": str(capture)})

            completed = subprocess.run(
                [str(launcher), "--no-browser", "--port", "19991"],
                check=False,
                capture_output=True,
                text=True,
                env=environment,
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertTrue(fake_python.is_file())
            self.assertEqual(
                capture.with_suffix(".args").read_text(encoding="utf-8").strip(),
                "-m whispertube.gui --no-browser --port 19991",
            )
            self.assertEqual(
                capture.with_suffix(".yt_dlp").read_text(encoding="utf-8").strip(),
                str(bin_dir / "yt-dlp"),
            )
            self.assertTrue(str(bin_dir) in capture.with_suffix(".path").read_text(encoding="utf-8"))

    def test_launch_fails_without_project_environment(self):
        with tempfile.TemporaryDirectory(prefix="whispertube release ") as directory:
            root = Path(directory)
            launcher = self._copy_script(root, "launch_macos.sh")
            completed = subprocess.run(
                [str(launcher), "--no-browser"],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("setup_macos.sh", completed.stderr)

    def test_setup_stops_before_creating_environment_on_failed_prerequisite(self):
        with tempfile.TemporaryDirectory(prefix="whispertube release ") as directory:
            root = Path(directory)
            setup = self._copy_script(root, "setup_macos.sh")
            fake_python = self._write_executable(
                root / "fake-python",
                """#!/bin/sh
exit 1
""",
            )
            environment = os.environ.copy()
            environment["PYTHON_BIN"] = str(fake_python)
            completed = subprocess.run(
                [str(setup)],
                check=False,
                capture_output=True,
                text=True,
                env=environment,
            )
            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("Setup stopped", completed.stderr)
            self.assertFalse((root / ".venv").exists())

    def test_setup_rerun_preserves_existing_runtime_files_in_path_with_spaces(self):
        with tempfile.TemporaryDirectory(prefix="whispertube release ") as directory:
            root = Path(directory)
            setup = self._copy_script(root, "setup_macos.sh")
            (root / "requirements-macos.txt").write_text("", encoding="utf-8")
            (root / "requirements-ui.txt").write_text("", encoding="utf-8")
            fake_python = self._write_executable(
                root / "fake-python",
                """#!/bin/sh
set -eu
if [ \"${1-}\" = \"-m\" ] && [ \"${2-}\" = \"whispertube.release\" ]; then exit 0; fi
if [ \"${1-}\" = \"-m\" ] && [ \"${2-}\" = \"pip\" ]; then exit 0; fi
exit 99
""",
            )
            venv_python = root / ".venv" / "bin" / "python"
            venv_python.parent.mkdir(parents=True)
            venv_python.symlink_to(fake_python)
            sentinel = root / "outputs" / "keep.md"
            sentinel.parent.mkdir()
            sentinel.write_text("keep", encoding="utf-8")
            environment = os.environ.copy()
            environment["PYTHON_BIN"] = str(fake_python)

            first = subprocess.run([str(setup)], check=False, capture_output=True, text=True, env=environment)
            second = subprocess.run([str(setup)], check=False, capture_output=True, text=True, env=environment)

            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertEqual(sentinel.read_text(encoding="utf-8"), "keep")


if __name__ == "__main__":
    unittest.main()
