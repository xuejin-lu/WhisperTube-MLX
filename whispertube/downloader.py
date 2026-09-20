"""Download best-available YouTube audio for local, manual use."""

from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Callable, TextIO
from urllib.parse import parse_qs, urlparse


_VIDEO_ID_LENGTH = 11
_PLAYLIST_ID_CHARS = frozenset("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-")
_VIDEO_ID_CHARS = _PLAYLIST_ID_CHARS
_YOUTUBE_HOSTS = frozenset({"youtube.com", "www.youtube.com", "m.youtube.com"})
_SHORT_HOSTS = frozenset({"youtu.be", "www.youtu.be"})
DOWNLOAD_MARKER = "__WHISPERTUBE_DOWNLOADED__:"


class RequestKind(str, Enum):
    VIDEO = "video"
    PLAYLIST = "playlist"


@dataclass(frozen=True)
class DownloadRequest:
    kind: RequestKind
    url: str
    output_root: Path
    cookies_from_browser: str | None = None


@dataclass(frozen=True)
class DownloadSummary:
    downloaded: int
    failed_or_skipped: int
    output_root: Path
    returncode: int


class DependencyError(Exception):
    """A required local executable is unavailable."""


def default_output_root() -> Path:
    return Path.home() / "Downloads" / "WhisperTube"


def _valid_video_id(value: str | None) -> bool:
    return bool(value) and len(value) == _VIDEO_ID_LENGTH and all(
        character in _VIDEO_ID_CHARS for character in value
    )


def _valid_playlist_id(value: str | None) -> bool:
    return bool(value) and all(character in _PLAYLIST_ID_CHARS for character in value)


def _request_root(output_root: str | Path | None) -> Path:
    return Path(output_root).expanduser() if output_root is not None else default_output_root()


def _canonical_video_url(parsed_url) -> str:
    path_parts = [part for part in parsed_url.path.split("/") if part]
    if parsed_url.hostname in _SHORT_HOSTS:
        video_id = path_parts[0] if path_parts else None
    elif parsed_url.path.rstrip("/") == "/watch":
        video_id = parse_qs(parsed_url.query).get("v", [None])[0]
    elif path_parts and path_parts[0] in {"shorts", "embed", "live"}:
        video_id = path_parts[1] if len(path_parts) > 1 else None
    else:
        video_id = None
    if not _valid_video_id(video_id):
        raise ValueError("YouTube URL does not contain a valid 11-character video ID")
    return f"https://www.youtube.com/watch?v={video_id}"


def classify_url(
    url: str,
    *,
    output_root: str | Path | None = None,
    cookies_from_browser: str | None = None,
) -> DownloadRequest:
    """Classify one explicit playlist or one single-video URL."""

    if not isinstance(url, str) or not url.strip():
        raise ValueError("YouTube URL cannot be empty")
    original = url.strip()
    parsed = urlparse(original)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("YouTube URL must use http:// or https://")
    hostname = (parsed.hostname or "").lower().rstrip(".")
    if hostname not in _YOUTUBE_HOSTS and hostname not in _SHORT_HOSTS:
        raise ValueError("URL must be from youtube.com or youtu.be")

    if hostname in _YOUTUBE_HOSTS and parsed.path.rstrip("/") == "/playlist":
        playlist_id = parse_qs(parsed.query).get("list", [None])[0]
        if not _valid_playlist_id(playlist_id):
            raise ValueError("YouTube playlist URL must include a valid list parameter")
        return DownloadRequest(
            RequestKind.PLAYLIST,
            original,
            _request_root(output_root),
            cookies_from_browser,
        )

    return DownloadRequest(
        RequestKind.VIDEO,
        _canonical_video_url(parsed),
        _request_root(output_root),
        cookies_from_browser,
    )


def _output_template(request: DownloadRequest) -> str:
    if request.kind is RequestKind.PLAYLIST:
        return str(
            request.output_root
            / "%(playlist)s"
            / "%(playlist_index)03d - %(title)s [%(id)s].%(ext)s"
        )
    return str(request.output_root / "%(title)s [%(id)s].%(ext)s")


def build_ytdlp_command(request: DownloadRequest, *, yt_dlp: str = "yt-dlp") -> list[str]:
    """Build argv without invoking a shell or adding conversion post-processors."""

    command = [yt_dlp]
    if request.kind is RequestKind.PLAYLIST:
        command.extend(["--yes-playlist", "--ignore-errors"])
    else:
        command.append("--no-playlist")
    command.extend(
        [
            "--format",
            "bestaudio",
            "--output",
            _output_template(request),
            "--newline",
            "--print",
            f"after_move:{DOWNLOAD_MARKER}%(filepath)s",
        ]
    )
    if request.cookies_from_browser:
        command.extend(["--cookies-from-browser", request.cookies_from_browser])
    command.append(request.url)
    return command


def _prepare_output_root(output_root: Path) -> None:
    try:
        output_root.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise OSError(f"cannot create output directory {output_root}: {exc}") from exc
    if not output_root.is_dir() or not output_root.exists():
        raise OSError(f"output path is not a directory: {output_root}")


PopenFactory = Callable[..., subprocess.Popen[str]]


def run_download(
    request: DownloadRequest,
    *,
    yt_dlp: str = "yt-dlp",
    popen_factory: PopenFactory = subprocess.Popen,
    output_stream: TextIO | None = None,
) -> DownloadSummary:
    """Run yt-dlp, stream its output, and print a concise completion summary."""

    stream = output_stream or sys.stdout
    _prepare_output_root(request.output_root)
    command = build_ytdlp_command(request, yt_dlp=yt_dlp)
    try:
        process = popen_factory(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
    except FileNotFoundError as exc:
        raise DependencyError(
            f"Cannot find {yt_dlp!r}; run scripts/setup_macos.sh or install yt-dlp."
        ) from exc

    downloaded = 0
    failed_or_skipped = 0
    for line in process.stdout or ():
        stream.write(line)
        if line.startswith(DOWNLOAD_MARKER):
            downloaded += 1
        if line.lstrip().startswith("ERROR:"):
            failed_or_skipped += 1
    returncode = process.wait()
    if returncode != 0 and failed_or_skipped == 0:
        failed_or_skipped = 1
    summary = DownloadSummary(downloaded, failed_or_skipped, request.output_root, returncode)
    print(f"Downloaded: {summary.downloaded}", file=stream)
    print(f"Failed/skipped: {summary.failed_or_skipped}", file=stream)
    print(f"Output: {summary.output_root}", file=stream)
    return summary


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Download best available YouTube audio for manual local use."
    )
    parser.add_argument("url", nargs="?", help="one YouTube video or explicit playlist URL")
    parser.add_argument("--output-root", type=Path, help="destination root (default: ~/Downloads/WhisperTube)")
    parser.add_argument("--cookies-from-browser", metavar="BROWSER")
    parser.add_argument("--yt-dlp", default="yt-dlp", help="yt-dlp executable or path")
    return parser


def main(
    argv: list[str] | None = None,
    *,
    input_fn: Callable[[str], str] = input,
    popen_factory: PopenFactory = subprocess.Popen,
) -> int:
    args = _build_parser().parse_args(argv)
    url = args.url
    if url is None:
        try:
            url = input_fn("Paste YouTube video or playlist URL: ")
        except EOFError:
            print("Input error: a YouTube URL is required.", file=sys.stderr)
            return 2
    try:
        request = classify_url(
            url,
            output_root=args.output_root,
            cookies_from_browser=args.cookies_from_browser,
        )
        summary = run_download(
            request,
            yt_dlp=args.yt_dlp,
            popen_factory=popen_factory,
        )
    except ValueError as exc:
        print(f"Input error: {exc}", file=sys.stderr)
        return 2
    except DependencyError as exc:
        print(f"Dependency error: {exc}", file=sys.stderr)
        return 127
    except OSError as exc:
        print(f"Output error: {exc}", file=sys.stderr)
        return 1
    return summary.returncode


if __name__ == "__main__":
    raise SystemExit(main())
