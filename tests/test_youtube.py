import unittest
from pathlib import Path

from whispertube.youtube import build_ytdlp_command, normalize_video_url


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
                "bestaudio/best",
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


if __name__ == "__main__":
    unittest.main()
