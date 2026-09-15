"""Normalize a single YouTube URL and download its best available audio."""

from __future__ import annotations

import argparse
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path
from urllib.parse import parse_qs, urlparse


_VIDEO_ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]{11}$")
_YOUTUBE_HOSTS = {"youtube.com", "www.youtube.com", "m.youtube.com"}
_SHORT_HOSTS = {"youtu.be", "www.youtu.be"}
_IGNORED_RUNTIME_ROOTS = {"temp", "outputs"}


def _validate_video_id(video_id: str | None) -> str:
    if video_id is None or not _VIDEO_ID_PATTERN.fullmatch(video_id):
        raise ValueError("URL does not contain a valid 11-character YouTube video ID")
    return video_id


def normalize_video_url(url: str) -> str:
    """Return a canonical single-video URL, ignoring playlist parameters."""

    if not isinstance(url, str) or not url.strip():
        raise ValueError("YouTube URL cannot be empty")

    parsed = urlparse(url.strip())
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("YouTube URL must use http:// or https://")

    hostname = (parsed.hostname or "").lower().rstrip(".")
    path_parts = [part for part in parsed.path.split("/") if part]

    if hostname in _SHORT_HOSTS:
        video_id = path_parts[0] if path_parts else None
    elif hostname in _YOUTUBE_HOSTS:
        if parsed.path.rstrip("/") == "/watch":
            video_id = parse_qs(parsed.query).get("v", [None])[0]
        elif path_parts and path_parts[0] in {"shorts", "embed", "live"}:
            video_id = path_parts[1] if len(path_parts) > 1 else None
        else:
            video_id = None
    else:
        raise ValueError("URL must be from youtube.com or youtu.be")

    return f"https://www.youtube.com/watch?v={_validate_video_id(video_id)}"


def build_ytdlp_command(
    url: str,
    output_dir: str | Path,
    *,
    yt_dlp: str = "yt-dlp",
    cookies_from_browser: str | None = None,
) -> list[str]:
    """Build a safe argv list for downloading one video's best available audio."""

    normalized_url = normalize_video_url(url)
    validated_output_dir = _validate_output_dir(output_dir)
    output_template = str(validated_output_dir / "%(title)s [%(id)s].%(ext)s")
    command = [
        yt_dlp,
        "--no-playlist",
        "--format",
        "bestaudio/best",
        "--output",
        output_template,
    ]
    if cookies_from_browser:
        command.extend(["--cookies-from-browser", cookies_from_browser])
    command.append(normalized_url)
    return command


def _validate_output_dir(output_dir: str | Path) -> Path:
    path = Path(output_dir)
    if not path.is_absolute() and (
        not path.parts or path.parts[0] not in _IGNORED_RUNTIME_ROOTS
    ):
        raise ValueError(
            "relative output directory must be under temp/ or outputs/; "
            "use an absolute system-temp path for other local locations"
        )
    return path


def _prepare_output_dir(output_dir: str | Path) -> Path:
    path = _validate_output_dir(output_dir)
    try:
        path.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise OSError(f"cannot create output directory: {exc}") from exc
    if not os.access(path, os.W_OK | os.X_OK):
        raise OSError("output directory is not writable")
    return path


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Download one YouTube video's best available audio locally."
    )
    parser.add_argument("url", help="YouTube watch, youtu.be, or Shorts URL")
    parser.add_argument(
        "--output-dir",
        default="temp/audio",
        help="Ignored directory for downloaded audio (default: temp/audio)",
    )
    parser.add_argument(
        "--cookies-from-browser",
        metavar="BROWSER",
        help="Use a local browser cookie source, for example safari",
    )
    parser.add_argument(
        "--yt-dlp",
        default="yt-dlp",
        help="yt-dlp executable to invoke (default: yt-dlp)",
    )
    parser.add_argument(
        "--print-command",
        action="store_true",
        help="Print the command without running it",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        command = build_ytdlp_command(
            args.url,
            args.output_dir,
            yt_dlp=args.yt_dlp,
            cookies_from_browser=args.cookies_from_browser,
        )
    except ValueError as exc:
        parser.error(str(exc))

    if args.print_command:
        print(shlex.join(command))
        return 0

    try:
        _prepare_output_dir(args.output_dir)
    except OSError as exc:
        print(
            f"Unable to use output directory {args.output_dir!r}: {exc}",
            file=sys.stderr,
        )
        return 1
    try:
        completed = subprocess.run(command, check=False)
    except FileNotFoundError:
        print(
            f"Cannot find {args.yt_dlp!r}; install yt-dlp or pass --yt-dlp PATH.",
            file=sys.stderr,
        )
        return 127
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
