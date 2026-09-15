import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from whispertube.youtube import build_ytdlp_command, main, normalize_video_url


VIDEO_ID = "gmj41fQTbfY"
CANONICAL_URL = f"https://www.youtube.com/watch?v={VIDEO_ID}"


class NormalizeVideoURLTests(unittest.TestCase):
    def test_watch_url(self) -> None:
        self.assertEqual(normalize_video_url(CANONICAL_URL), CANONICAL_URL)

    def test_short_url_with_timestamp(self) -> None:
        url = f"https://youtu.be/{VIDEO_ID}?t=42"
        self.assertEqual(normalize_video_url(url), CANONICAL_URL)

    def test_shorts_url(self) -> None:
        self.assertEqual(
            normalize_video_url(f"https://www.youtube.com/shorts/{VIDEO_ID}"),
            CANONICAL_URL,
        )

    def test_playlist_parameters_are_ignored(self) -> None:
        url = f"https://www.youtube.com/watch?v={VIDEO_ID}&list=PL123&index=2"
        self.assertEqual(normalize_video_url(url), CANONICAL_URL)

    def test_non_youtube_url_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            normalize_video_url("https://example.com/watch?v=gmj41fQTbfY")


class BuildYTDLPCommandTests(unittest.TestCase):
    def test_builds_single_video_command(self) -> None:
        command = build_ytdlp_command(CANONICAL_URL, Path("temp/audio"))
        self.assertEqual(
            command,
            [
                "yt-dlp",
                "--no-playlist",
                "--format",
                "bestaudio",
                "--output",
                "temp/audio/%(title)s [%(id)s].%(ext)s",
                CANONICAL_URL,
            ],
        )

    def test_adds_browser_cookie_fallback(self) -> None:
        command = build_ytdlp_command(
            CANONICAL_URL,
            "temp/audio",
            cookies_from_browser="safari",
        )
        self.assertIn("--no-playlist", command)
        self.assertEqual(command[-3:], ["--cookies-from-browser", "safari", CANONICAL_URL])

    def test_browser_fallback_does_not_export_cookie_file(self) -> None:
        command = build_ytdlp_command(
            CANONICAL_URL,
            "temp/audio",
            cookies_from_browser="safari",
        )
        self.assertNotIn("--cookies", command)


class CLITests(unittest.TestCase):
    def test_print_command_uses_canonical_single_video_url(self) -> None:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = main(
                [
                    f"https://www.youtube.com/watch?v={VIDEO_ID}&list=PL123",
                    "--output-dir",
                    "temp/audio",
                    "--print-command",
                ]
            )

        self.assertEqual(result, 0)
        self.assertIn("--no-playlist", output.getvalue())
        self.assertIn(CANONICAL_URL, output.getvalue())
        self.assertNotIn("list=PL123", output.getvalue())

    def test_missing_downloader_returns_127(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch(
                "whispertube.youtube.subprocess.run",
                side_effect=FileNotFoundError,
            ):
                result = main(
                    [CANONICAL_URL, "--output-dir", str(Path(temp_dir) / "audio")]
                )

        self.assertEqual(result, 127)

    def test_downloader_failure_exit_code_is_propagated(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch(
                "whispertube.youtube.subprocess.run",
                return_value=unittest.mock.Mock(returncode=23),
            ):
                result = main(
                    [CANONICAL_URL, "--output-dir", str(Path(temp_dir) / "audio")]
                )

        self.assertEqual(result, 23)

    def test_unwritable_output_directory_fails_before_downloader(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_target = Path(temp_dir) / "not-a-directory"
            output_target.write_text("occupied", encoding="utf-8")
            error = io.StringIO()
            with patch("whispertube.youtube.subprocess.run") as run:
                with contextlib.redirect_stderr(error):
                    result = main([CANONICAL_URL, "--output-dir", str(output_target)])

        self.assertEqual(result, 1)
        self.assertIn("output directory", error.getvalue().lower())
        run.assert_not_called()

    def test_invalid_url_fails_before_downloader(self) -> None:
        error = io.StringIO()
        with patch("whispertube.youtube.subprocess.run") as run:
            with self.assertRaises(SystemExit) as raised:
                with contextlib.redirect_stderr(error):
                    main(["https://example.com/video"])

        self.assertEqual(raised.exception.code, 2)
        run.assert_not_called()

    def test_unsafe_relative_output_path_fails_before_downloader(self) -> None:
        error = io.StringIO()
        with patch("whispertube.youtube.subprocess.run") as run:
            with self.assertRaises(SystemExit) as raised:
                with contextlib.redirect_stderr(error):
                    main([CANONICAL_URL, "--output-dir", "downloads/audio"])

        self.assertEqual(raised.exception.code, 2)
        self.assertIn("temp/", error.getvalue())
        run.assert_not_called()

    def test_relative_output_path_traversal_fails_before_downloader(self) -> None:
        error = io.StringIO()
        with patch("whispertube.youtube.subprocess.run") as run:
            with self.assertRaises(SystemExit) as raised:
                with contextlib.redirect_stderr(error):
                    main(
                        [
                            CANONICAL_URL,
                            "--output-dir",
                            "temp/../../outside",
                            "--print-command",
                        ]
                    )

        self.assertEqual(raised.exception.code, 2)
        self.assertIn("temp/", error.getvalue())
        run.assert_not_called()


if __name__ == "__main__":
    unittest.main()
