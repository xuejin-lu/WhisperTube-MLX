from __future__ import annotations

import contextlib
import io
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock

from whispertube.downloader import (
    DOWNLOAD_MARKER,
    RequestKind,
    build_ytdlp_command,
    classify_url,
    main,
    run_download,
)


VIDEO_ID = "gmj41fQTbfY"
VIDEO_URL = f"https://www.youtube.com/watch?v={VIDEO_ID}"
PLAYLIST_URL = "https://www.youtube.com/playlist?list=PL1234567890"


class URLClassificationTests(unittest.TestCase):
    def test_video_forms_are_normalized_and_playlist_is_explicit(self) -> None:
        for url in (
            VIDEO_URL,
            f"https://youtu.be/{VIDEO_ID}?t=42",
            f"https://www.youtube.com/shorts/{VIDEO_ID}",
            f"https://www.youtube.com/live/{VIDEO_ID}",
            f"https://www.youtube.com/embed/{VIDEO_ID}",
        ):
            request = classify_url(url)
            self.assertEqual(request.kind, RequestKind.VIDEO)
            self.assertEqual(request.url, VIDEO_URL)

        playlist = classify_url(PLAYLIST_URL)
        self.assertEqual(playlist.kind, RequestKind.PLAYLIST)
        self.assertEqual(playlist.url, PLAYLIST_URL)

    def test_watch_url_with_list_query_remains_single_video(self) -> None:
        request = classify_url(f"{VIDEO_URL}&list=PL1234567890&index=2")
        self.assertEqual(request.kind, RequestKind.VIDEO)
        self.assertEqual(request.url, VIDEO_URL)

    def test_invalid_urls_are_rejected(self) -> None:
        for url in (
            "https://example.com/watch?v=gmj41fQTbfY",
            "ftp://www.youtube.com/watch?v=gmj41fQTbfY",
            "https://www.youtube.com/watch?v=short",
            "https://www.youtube.com/playlist",
        ):
            with self.subTest(url=url), self.assertRaises(ValueError):
                classify_url(url)


class CommandConstructionTests(unittest.TestCase):
    def test_video_command_is_single_video_bestaudio_without_mp3_conversion(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            request = classify_url(VIDEO_URL, output_root=Path(directory))
            command = build_ytdlp_command(request, yt_dlp="project-yt-dlp")

        self.assertEqual(command[0], "project-yt-dlp")
        self.assertIn("--no-playlist", command)
        self.assertIn("--format", command)
        self.assertIn("bestaudio", command)
        self.assertIn("%(title)s [%(id)s].%(ext)s", command[command.index("--output") + 1])
        self.assertNotIn("--extract-audio", command)
        self.assertNotIn("mp3", " ".join(command).lower())
        self.assertEqual(command[-1], VIDEO_URL)

    def test_playlist_command_is_ordered_and_continues_errors(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            request = classify_url(PLAYLIST_URL, output_root=Path(directory))
            command = build_ytdlp_command(request)

        self.assertEqual(command[0], "yt-dlp")
        self.assertIn("--yes-playlist", command)
        self.assertIn("--ignore-errors", command)
        output = command[command.index("--output") + 1]
        self.assertIn("%(playlist)s", output)
        self.assertIn("%(playlist_index)03d", output)
        self.assertIn("%(title)s [%(id)s].%(ext)s", output)
        self.assertEqual(command[-1], PLAYLIST_URL)

    def test_browser_cookie_option_is_explicit_only(self) -> None:
        request = classify_url(VIDEO_URL, cookies_from_browser="safari")
        command = build_ytdlp_command(request)
        self.assertIn(["--cookies-from-browser", "safari"], [command[i : i + 2] for i in range(len(command) - 1)])


class FakeProcess:
    def __init__(self, lines: list[str], returncode: int = 0) -> None:
        self.stdout = iter(lines)
        self.returncode = returncode

    def wait(self) -> int:
        return self.returncode


class RunnerTests(unittest.TestCase):
    def test_runner_streams_progress_and_prints_summary(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            request = classify_url(VIDEO_URL, output_root=Path(directory))
            output = io.StringIO()
            process = FakeProcess(
                [
                    "[download] 100%\n",
                    f"{DOWNLOAD_MARKER}{Path(directory) / 'title [id].webm'}\n",
                ]
            )
            popen = Mock(return_value=process)
            summary = run_download(request, popen_factory=popen, output_stream=output)

        self.assertEqual(summary.downloaded, 1)
        self.assertEqual(summary.failed_or_skipped, 0)
        self.assertEqual(summary.returncode, 0)
        self.assertIn("[download] 100%", output.getvalue())
        self.assertIn("Downloaded: 1", output.getvalue())
        popen.assert_called_once()
        self.assertNotIn("shell", popen.call_args.kwargs)

    def test_playlist_runner_reports_errors_and_keeps_success_status(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            request = classify_url(PLAYLIST_URL, output_root=Path(directory))
            output = io.StringIO()
            process = FakeProcess(
                [
                    f"{DOWNLOAD_MARKER}/tmp/001.webm\n",
                    "ERROR: unavailable\n",
                    f"{DOWNLOAD_MARKER}/tmp/003.m4a\n",
                ]
            )
            summary = run_download(request, popen_factory=Mock(return_value=process), output_stream=output)

        self.assertEqual(summary.downloaded, 2)
        self.assertEqual(summary.failed_or_skipped, 1)
        self.assertEqual(summary.returncode, 0)
        self.assertIn("Failed/skipped: 1", output.getvalue())

    def test_missing_yt_dlp_is_actionable(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            error = io.StringIO()
            with contextlib.redirect_stderr(error):
                result = main([VIDEO_URL, "--output-root", directory], popen_factory=Mock(side_effect=FileNotFoundError))

        self.assertEqual(result, 127)
        self.assertIn("yt-dlp", error.getvalue())

    def test_main_invalid_url_does_not_invoke_process(self) -> None:
        popen = Mock()
        error = io.StringIO()
        with contextlib.redirect_stderr(error):
            result = main(["https://example.com/video"], popen_factory=popen)

        self.assertEqual(result, 2)
        self.assertIn("URL", error.getvalue())
        popen.assert_not_called()


class ActiveScopeTests(unittest.TestCase):
    def _copy_executable(self, source: Path, destination: Path) -> Path:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        destination.chmod(0o755)
        return destination

    def test_launcher_finds_project_yt_dlp_with_clean_path_and_spaces(self) -> None:
        root = Path(__file__).parents[1]
        with tempfile.TemporaryDirectory(prefix="downloader path ") as directory:
            project = Path(directory)
            launcher = self._copy_executable(root / "scripts/launch_macos.sh", project / "scripts/launch_macos.sh")
            fake_python = project / ".venv/bin/python"
            fake_python.parent.mkdir(parents=True)
            fake_python.write_text(
                "#!/bin/sh\n"
                "set -eu\n"
                "printf '%s\\n' \"$*\" > \"$CAPTURE.args\"\n"
                "command -v yt-dlp > \"$CAPTURE.yt-dlp\"\n",
                encoding="utf-8",
            )
            fake_python.chmod(0o755)
            yt_dlp = project / ".venv/bin/yt-dlp"
            yt_dlp.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
            yt_dlp.chmod(0o755)
            environment = {"PATH": "/usr/bin:/bin", "CAPTURE": str(project / "capture")}
            completed = subprocess.run(
                [str(launcher), "--output-root", "/tmp/space safe"],
                check=False,
                capture_output=True,
                text=True,
                env=environment,
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertEqual(
                (project / "capture.args").read_text(encoding="utf-8").strip(),
                "-m whispertube.downloader --output-root /tmp/space safe",
            )
            self.assertEqual(
                (project / "capture.yt-dlp").read_text(encoding="utf-8").strip(),
                str(yt_dlp),
            )

    def test_setup_rerun_does_not_delete_existing_user_file(self) -> None:
        root = Path(__file__).parents[1]
        with tempfile.TemporaryDirectory(prefix="downloader setup path ") as directory:
            project = Path(directory)
            setup = self._copy_executable(root / "scripts/setup_macos.sh", project / "scripts/setup_macos.sh")
            (project / "requirements-macos.txt").write_text("", encoding="utf-8")
            fake_python = project / "fake-python"
            fake_python.write_text(
                "#!/bin/sh\n"
                "set -eu\n"
                "if [ \"${1-}\" = \"-m\" ] && [ \"${2-}\" = \"pip\" ]; then exit 0; fi\n"
                "exit 99\n",
                encoding="utf-8",
            )
            fake_python.chmod(0o755)
            venv_python = project / ".venv/bin/python"
            venv_python.parent.mkdir(parents=True)
            venv_python.symlink_to(fake_python)
            sentinel = project / "Downloads/keep.webm"
            sentinel.parent.mkdir()
            sentinel.write_bytes(b"keep")
            environment = {"PYTHON_BIN": str(fake_python), "PATH": "/usr/bin:/bin"}

            first = subprocess.run([str(setup)], check=False, capture_output=True, text=True, env=environment)
            second = subprocess.run([str(setup)], check=False, capture_output=True, text=True, env=environment)

            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertEqual(sentinel.read_bytes(), b"keep")

    def test_downloader_source_has_no_obsolete_runtime_imports(self) -> None:
        source = Path(__file__).parents[1] / "whispertube/downloader.py"
        text = source.read_text(encoding="utf-8")
        for forbidden in ("mlx", "mlx_whisper", "opencc", "gradio", "whispertube.pipeline", "localhost"):
            self.assertNotIn(forbidden, text.lower())

    def test_launcher_is_shell_safe_and_does_not_start_gui(self) -> None:
        root = Path(__file__).parents[1]
        launcher = (root / "DownloadAudio.command").read_text(encoding="utf-8")
        self.assertIn("scripts/launch_macos.sh", launcher)
        self.assertNotIn("whispertube.gui", launcher)
        self.assertNotIn("--share", launcher)
        self.assertNotIn("0.0.0.0", launcher)


if __name__ == "__main__":
    unittest.main()
