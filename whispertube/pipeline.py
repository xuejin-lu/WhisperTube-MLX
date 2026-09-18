"""Compose local YouTube acquisition and MLX transcription."""

from __future__ import annotations

import argparse
import os
import sys
import tempfile
from pathlib import Path
from typing import Callable

from whispertube import youtube
from whispertube.transcription import (
    DEFAULT_MODEL,
    DEFAULT_OUTPUT_DIR,
    TranscriptionError,
    transcribe_audio,
)


DEFAULT_AUDIO_DIR = "temp/pipeline-audio"
_RUNTIME_ROOTS = {"temp", "outputs"}


class PipelineError(Exception):
    exit_code = 1
    category = "pipeline"


class DownloadError(PipelineError):
    exit_code = 2
    category = "download"


class CleanupError(PipelineError):
    exit_code = 7
    category = "cleanup"


Acquire = Callable[..., Path]
Transcribe = Callable[..., Path]


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def _prepare_audio_root(audio_dir: str | Path) -> Path:
    path = Path(audio_dir)
    if path.is_absolute():
        resolved = path.resolve(strict=False)
        if not _is_within(resolved, Path(tempfile.gettempdir()).resolve()):
            raise DownloadError("absolute audio directory must be under the system temporary directory")
    else:
        path = Path(os.path.normpath(str(path)))
        if not path.parts or path.parts[0] not in _RUNTIME_ROOTS:
            raise DownloadError("audio directory must be under temp/ or outputs/")
    try:
        path.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise DownloadError(f"cannot create temporary audio directory: {exc}") from exc
    if not path.is_dir() or not os.access(path, os.W_OK | os.X_OK):
        raise DownloadError(f"temporary audio directory is not writable: {path}")
    return path


def _default_acquire(
    url: str,
    *,
    audio_dir: str | Path,
    cookies_from_browser: str | None,
    yt_dlp: str,
) -> Path:
    root = _prepare_audio_root(audio_dir)
    run_dir = Path(tempfile.mkdtemp(prefix="run-", dir=root))
    argv = [url, "--output-dir", str(run_dir), "--yt-dlp", yt_dlp]
    if cookies_from_browser:
        argv.extend(["--cookies-from-browser", cookies_from_browser])
    try:
        result = youtube.main(argv)
    except SystemExit as exc:
        raise DownloadError(f"invalid download request (exit {exc.code})") from exc
    if result != 0:
        raise DownloadError(f"YouTube acquisition failed with exit code {result}")
    artifacts = [path for path in run_dir.iterdir() if path.is_file()]
    if len(artifacts) != 1:
        raise DownloadError(f"acquisition produced {len(artifacts)} files; expected exactly one")
    return artifacts[0]


def run_pipeline(
    url: str,
    *,
    audio_dir: str | Path = DEFAULT_AUDIO_DIR,
    output_dir: str | Path = DEFAULT_OUTPUT_DIR,
    model: str = DEFAULT_MODEL,
    cookies_from_browser: str | None = None,
    yt_dlp: str = "yt-dlp",
    acquire: Acquire | None = None,
    transcribe: Transcribe | None = None,
) -> Path:
    """Run both approved stages and remove only this run's acquired audio."""

    root = _prepare_audio_root(audio_dir)
    acquirer = acquire or _default_acquire
    transcriber = transcribe or transcribe_audio
    owned_audio: Path | None = None
    failed = False
    try:
        try:
            candidate = Path(
                acquirer(
                    url,
                    audio_dir=audio_dir,
                    cookies_from_browser=cookies_from_browser,
                    yt_dlp=yt_dlp,
                )
            )
        except DownloadError:
            raise
        except (Exception, SystemExit) as exc:
            raise DownloadError(f"YouTube acquisition failed: {exc}") from exc
        resolved = candidate.resolve(strict=False)
        if not _is_within(resolved, root.resolve()):
            raise DownloadError("acquisition returned audio outside the owned temporary directory")
        if not candidate.is_file():
            raise DownloadError("acquisition did not return a regular audio file")
        owned_audio = candidate
        return Path(transcriber(candidate, output_dir=output_dir, model=model))
    except Exception:
        failed = True
        raise
    finally:
        if owned_audio is not None:
            try:
                owned_audio.unlink(missing_ok=True)
                if owned_audio.parent != root and owned_audio.parent.name.startswith("run-"):
                    try:
                        owned_audio.parent.rmdir()
                    except OSError:
                        pass
            except OSError as exc:
                if not failed:
                    raise CleanupError(f"cannot remove temporary audio {owned_audio}: {exc}") from exc


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Download and transcribe one YouTube video locally.")
    parser.add_argument("url")
    parser.add_argument("--audio-dir", default=DEFAULT_AUDIO_DIR)
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--cookies-from-browser")
    parser.add_argument("--yt-dlp", default="yt-dlp")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        output = run_pipeline(
            args.url,
            audio_dir=args.audio_dir,
            output_dir=args.output_dir,
            model=args.model,
            cookies_from_browser=args.cookies_from_browser,
            yt_dlp=args.yt_dlp,
        )
    except (PipelineError, TranscriptionError) as exc:
        print(f"{exc.category} error: {exc}", file=sys.stderr)
        return exc.exit_code
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
