"""Transcribe one local audio file with MLX Whisper."""

from __future__ import annotations

import argparse
import os
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Callable, Any


DEFAULT_MODEL = "mlx-community/whisper-large-v3-mlx"
DEFAULT_OUTPUT_DIR = "temp/transcripts"
DEFAULT_LANGUAGE = "zh"
_IGNORED_RUNTIME_ROOTS = {"temp", "outputs"}
SUPPORTED_AUDIO_SUFFIXES = (
    ".aac",
    ".flac",
    ".m4a",
    ".mp3",
    ".ogg",
    ".wav",
    ".webm",
)
_SUPPORTED_AUDIO_SUFFIXES = set(SUPPORTED_AUDIO_SUFFIXES)
_STRONG_PARAGRAPH_BOUNDARIES = "。！？!?；;\n"
_WEAK_PARAGRAPH_BOUNDARIES = "：:，,、"


class TranscriptionError(Exception):
    """Base class for errors that can be reported by the CLI."""

    exit_code = 1
    category = "transcription"


class InputError(TranscriptionError):
    exit_code = 2
    category = "input"


class DependencyError(TranscriptionError):
    exit_code = 3
    category = "dependency"


class ModelError(TranscriptionError):
    exit_code = 4
    category = "model"


class InferenceError(TranscriptionError):
    exit_code = 5
    category = "inference"


class OutputError(TranscriptionError):
    exit_code = 6
    category = "output"


Transcriber = Callable[..., dict[str, Any]]
TextConverter = Callable[[str], str]


def _validate_input(input_path: str | Path) -> Path:
    path = Path(input_path)
    if not path.exists():
        raise InputError(f"audio input does not exist: {path}")
    if not path.is_file():
        raise InputError(f"audio input is not a regular file: {path}")
    if not os.access(path, os.R_OK):
        raise InputError(f"audio input is not readable: {path}")
    if path.suffix.lower() not in _SUPPORTED_AUDIO_SUFFIXES:
        raise InputError(f"unsupported audio format: {path.suffix or '<none>'}")
    return path


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def _validate_output_dir(output_dir: str | Path) -> Path:
    path = Path(output_dir)
    if path.is_absolute():
        resolved = path.resolve(strict=False)
        system_temp = Path(tempfile.gettempdir()).resolve()
        if not _is_within(resolved, system_temp):
            raise OutputError(
                "absolute output directory must be under the local system temporary directory"
            )
        return path

    normalized = Path(os.path.normpath(str(path)))
    if not normalized.parts or normalized.parts[0] not in _IGNORED_RUNTIME_ROOTS:
        raise OutputError("relative output directory must be under temp/ or outputs/")
    return normalized


def _prepare_output_dir(output_dir: str | Path) -> Path:
    path = _validate_output_dir(output_dir)
    try:
        path.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise OutputError(f"cannot create output directory {path}: {exc}") from exc
    if not path.is_dir() or not os.access(path, os.W_OK | os.X_OK):
        raise OutputError(f"output directory is not writable: {path}")
    return path


def _load_transcriber() -> Transcriber:
    try:
        import mlx_whisper
    except ImportError as exc:
        raise DependencyError(
            "mlx-whisper is not installed; install requirements-macos.txt"
        ) from exc
    return mlx_whisper.transcribe


def _load_converter() -> TextConverter:
    try:
        from opencc import OpenCC
    except ImportError as exc:
        raise DependencyError("OpenCC is not installed; install requirements-macos.txt") from exc
    return OpenCC("s2tw").convert


def _ensure_ffmpeg_available() -> None:
    if shutil.which("ffmpeg") is None:
        raise DependencyError("ffmpeg is not available on PATH; install ffmpeg locally")


def _is_dependency_error(exc: Exception) -> bool:
    message = str(exc).lower()
    return "ffmpeg" in message or "decoder" in message or "avformat" in message


def _is_model_error(exc: Exception) -> bool:
    message = str(exc).lower()
    model_terms = (
        "model",
        "checkpoint",
        "config",
        "repository",
        "repo",
        "weights",
        "tokenizer",
        "huggingface",
        "safetensors",
    )
    return isinstance(exc, (FileNotFoundError, IsADirectoryError, KeyError)) or any(
        term in message for term in model_terms
    )


def _paragraph_end(text: str, start: int, max_chars: int) -> int:
    hard_end = min(start + max_chars, len(text))
    if hard_end == len(text):
        return hard_end

    search_start = start + max(1, int(max_chars * 0.75))
    for index in range(hard_end - 1, search_start - 1, -1):
        if text[index] in _STRONG_PARAGRAPH_BOUNDARIES:
            return index + 1

    lookahead_end = min(len(text), start + max_chars + max_chars // 4)
    for index in range(hard_end, lookahead_end):
        if text[index] in _STRONG_PARAGRAPH_BOUNDARIES:
            return index + 1

    for index in range(hard_end - 1, search_start - 1, -1):
        if text[index] in _WEAK_PARAGRAPH_BOUNDARIES:
            return index + 1
    return hard_end


def format_paragraphs(text: str, *, max_chars: int = 500) -> str:
    """Wrap transcript text into bounded readable paragraphs without summarizing it."""

    if max_chars < 1:
        raise ValueError("max_chars must be positive")
    normalized = " ".join(text.split())
    paragraphs: list[str] = []
    start = 0
    while start < len(normalized):
        end = _paragraph_end(normalized, start, max_chars)
        paragraphs.append(normalized[start:end])
        start = end
    return "\n\n".join(paragraphs)


def _render_markdown(source: Path, model: str, language: str, text: str) -> str:
    def inline(value: str) -> str:
        return value.replace("`", "\\`").replace("\n", " ")

    return (
        "# Transcript\n\n"
        f"- Source: `{inline(source.name)}`\n"
        f"- Model: `{inline(model)}`\n"
        f"- Language: `{inline(language)}`\n"
        "- Task: `transcribe`\n\n"
        "## Transcript\n\n"
        f"{format_paragraphs(text)}\n"
    )


def transcribe_audio(
    input_path: str | Path,
    *,
    output_dir: str | Path = DEFAULT_OUTPUT_DIR,
    model: str = DEFAULT_MODEL,
    language: str = DEFAULT_LANGUAGE,
    transcriber: Transcriber | None = None,
    converter: TextConverter | None = None,
) -> Path:
    """Transcribe one local audio file and return its newly written Markdown path."""

    if language != DEFAULT_LANGUAGE:
        raise InputError("only Chinese transcription language 'zh' is supported in v0.2")

    source = _validate_input(input_path)
    destination_dir = _prepare_output_dir(output_dir)
    destination = destination_dir / f"{source.stem}.md"
    if destination.exists():
        raise OutputError(f"transcript already exists; refusing to overwrite: {destination}")

    if transcriber is None:
        _ensure_ffmpeg_available()
    backend = transcriber or _load_transcriber()
    text_converter = converter or _load_converter()
    try:
        result = backend(
            str(source),
            path_or_hf_repo=model,
            language=language,
            task="transcribe",
            verbose=False,
        )
    except TranscriptionError:
        raise
    except Exception as exc:
        if _is_dependency_error(exc):
            raise DependencyError(f"local audio dependency failed: {exc}") from exc
        if _is_model_error(exc):
            raise ModelError(f"unable to load model {model!r}: {exc}") from exc
        raise InferenceError(f"local transcription failed: {exc}") from exc

    text = result.get("text") if isinstance(result, dict) else None
    if not isinstance(text, str) or not text.strip():
        raise InferenceError("local transcription returned no text")
    try:
        traditional_text = text_converter(text).strip()
    except Exception as exc:
        raise InferenceError(f"transcript text conversion failed: {exc}") from exc
    if not traditional_text:
        raise InferenceError("transcript text conversion returned no text")

    content = _render_markdown(source, model, language, traditional_text)
    try:
        with destination.open("x", encoding="utf-8") as output:
            output.write(content)
    except FileExistsError as exc:
        raise OutputError(f"transcript already exists; refusing to overwrite: {destination}") from exc
    except OSError as exc:
        raise OutputError(f"cannot write transcript {destination}: {exc}") from exc
    return destination


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Transcribe one local audio file with MLX Whisper.")
    parser.add_argument("input", help="local audio file")
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--language", default=DEFAULT_LANGUAGE, choices=(DEFAULT_LANGUAGE,))
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        output = transcribe_audio(
            args.input,
            output_dir=args.output_dir,
            model=args.model,
            language=args.language,
        )
    except TranscriptionError as exc:
        print(f"{exc.category} error: {exc}", file=sys.stderr)
        return exc.exit_code
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
