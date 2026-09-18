"""Local graphical interface over the approved end-to-end pipeline."""

from __future__ import annotations

import argparse
import os
import tempfile
from dataclasses import dataclass
from enum import Enum
from functools import partial
from pathlib import Path
from typing import Callable

from whispertube.pipeline import DEFAULT_AUDIO_DIR, PipelineError, run_pipeline
from whispertube.transcription import DEFAULT_MODEL, DEFAULT_OUTPUT_DIR, TranscriptionError


LOCAL_SERVER_NAME = "127.0.0.1"
DEFAULT_GUI_PORT = 7860
GUI_TITLE = "WhisperTube MLX"
_RUNTIME_ROOTS = {"temp", "outputs"}

Pipeline = Callable[..., Path]


class TranscriptResultError(Exception):
    """The pipeline returned a transcript that is unsafe to expose in the GUI."""


class GUIStatus(str, Enum):
    IDLE = "idle"
    RUNNING = "running"
    SUCCESS = "success"
    ERROR = "error"


@dataclass(frozen=True)
class GUIResult:
    status: GUIStatus
    message: str
    preview: str = ""
    transcript_path: Path | None = None
    action_enabled: bool = True


DEFAULT_AUDIO_ROOT = Path(DEFAULT_AUDIO_DIR)
DEFAULT_TRANSCRIPT_ROOT = Path(DEFAULT_OUTPUT_DIR)


def begin_run() -> GUIResult:
    """Return the visible state shown before pipeline work begins."""

    return GUIResult(
        status=GUIStatus.RUNNING,
        message="Transcription is running locally…",
        action_enabled=False,
    )


def execute_pipeline_request(
    url: str,
    *,
    model: str = DEFAULT_MODEL,
    audio_dir: str | Path = DEFAULT_AUDIO_ROOT,
    output_dir: str | Path = DEFAULT_TRANSCRIPT_ROOT,
    pipeline: Pipeline = run_pipeline,
) -> Path:
    """Validate the GUI request and invoke the approved pipeline exactly once."""

    normalized_url = url.strip()
    if not normalized_url:
        raise ValueError("YouTube URL is required")
    return Path(
        pipeline(
            normalized_url,
            model=model,
            audio_dir=audio_dir,
            output_dir=output_dir,
        )
    )


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def _approved_transcript_root(output_dir: str | Path, *, create: bool = False) -> Path:
    path = Path(output_dir)
    if path.is_absolute():
        resolved = path.resolve(strict=False)
        if not _is_within(resolved, Path(tempfile.gettempdir()).resolve()):
            raise ValueError("transcript directory must be under the local system temporary directory")
    else:
        normalized = Path(os.path.normpath(str(path)))
        if not normalized.parts or normalized.parts[0] not in _RUNTIME_ROOTS:
            raise ValueError("transcript directory must be under temp/ or outputs/")
        resolved = normalized.resolve(strict=False)
        runtime_root = Path(normalized.parts[0]).resolve(strict=False)
        if not _is_within(resolved, runtime_root):
            raise ValueError("transcript directory escapes its approved runtime root")
    if create:
        resolved.mkdir(parents=True, exist_ok=True)
    return resolved


def load_transcript_result(path: Path, output_dir: str | Path) -> tuple[Path, str]:
    """Validate and load one GUI-safe Markdown transcript."""

    resolved = path.resolve(strict=False)
    try:
        root = _approved_transcript_root(output_dir)
    except ValueError as exc:
        raise TranscriptResultError("transcript output directory is not approved") from exc
    if not _is_within(resolved, root):
        raise TranscriptResultError("transcript is outside the approved output directory")
    if resolved.suffix.lower() != ".md":
        raise TranscriptResultError("transcript must be a Markdown file")
    if not resolved.is_file():
        raise TranscriptResultError("transcript file is missing")
    try:
        content = resolved.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise TranscriptResultError("transcript is not readable UTF-8") from exc
    if not content.strip():
        raise TranscriptResultError("transcript is empty")
    return resolved, content


def _component_values(result: GUIResult):
    import gradio as gr

    download = str(result.transcript_path) if result.transcript_path is not None else None
    return result.message, result.preview, download, gr.Button(interactive=result.action_enabled)


def _begin_component_values():
    return _component_values(begin_run())


def _basic_terminal_values(
    url: str,
    *,
    model: str,
    audio_dir: str | Path,
    output_dir: str | Path,
    pipeline: Pipeline,
):
    return _component_values(
        run_gui_request(
            url,
            model=model,
            audio_dir=audio_dir,
            output_dir=output_dir,
            pipeline=pipeline,
        )
    )


def run_gui_request(
    url: str,
    *,
    model: str = DEFAULT_MODEL,
    audio_dir: str | Path = DEFAULT_AUDIO_ROOT,
    output_dir: str | Path = DEFAULT_TRANSCRIPT_ROOT,
    pipeline: Pipeline = run_pipeline,
) -> GUIResult:
    """Return a safe terminal GUI result for one approved pipeline invocation."""

    try:
        transcript = execute_pipeline_request(
            url,
            model=model,
            audio_dir=audio_dir,
            output_dir=output_dir,
            pipeline=pipeline,
        )
    except ValueError as exc:
        return GUIResult(GUIStatus.ERROR, f"input error: {exc}")
    except (PipelineError, TranscriptionError) as exc:
        return GUIResult(GUIStatus.ERROR, f"{exc.category} error: {exc}")
    except Exception:
        return GUIResult(GUIStatus.ERROR, "application error: unexpected local failure")
    try:
        transcript, preview = load_transcript_result(transcript, output_dir)
    except TranscriptResultError as exc:
        return GUIResult(GUIStatus.ERROR, f"output error: {exc}")
    return GUIResult(
        status=GUIStatus.SUCCESS,
        message=f"Success: {transcript.name}",
        preview=preview,
        transcript_path=transcript,
    )


def launch_app(
    app,
    *,
    output_dir: str | Path = DEFAULT_TRANSCRIPT_ROOT,
    port: int = DEFAULT_GUI_PORT,
    inbrowser: bool = True,
):
    """Launch a Blocks app with explicit local-only privacy settings."""

    transcript_root = _approved_transcript_root(output_dir, create=True)
    return app.launch(
        server_name=LOCAL_SERVER_NAME,
        server_port=port,
        share=False,
        inbrowser=inbrowser,
        show_error=False,
        enable_monitoring=False,
        strict_cors=True,
        allowed_paths=[str(transcript_root.resolve())],
        footer_links=[],
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run WhisperTube's local graphical interface.")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--audio-dir", default=DEFAULT_AUDIO_ROOT)
    parser.add_argument("--output-dir", default=DEFAULT_TRANSCRIPT_ROOT)
    parser.add_argument("--port", type=int, default=DEFAULT_GUI_PORT)
    parser.add_argument("--no-browser", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    app = build_app(
        model=args.model,
        audio_dir=args.audio_dir,
        output_dir=args.output_dir,
    )
    launch_app(
        app,
        output_dir=args.output_dir,
        port=args.port,
        inbrowser=not args.no_browser,
    )
    return 0


def build_app(
    *,
    model: str = DEFAULT_MODEL,
    audio_dir: str | Path = DEFAULT_AUDIO_ROOT,
    output_dir: str | Path = DEFAULT_TRANSCRIPT_ROOT,
    pipeline: Pipeline = run_pipeline,
    handler: Callable | None = None,
):
    """Build the local Blocks interface without starting a server."""

    import gradio as gr

    terminal_handler = handler or partial(
        _basic_terminal_values,
        model=model,
        audio_dir=audio_dir,
        output_dir=output_dir,
        pipeline=pipeline,
    )
    with gr.Blocks(title=GUI_TITLE, analytics_enabled=False, delete_cache=(3600, 3600)) as app:
        gr.Markdown("# WhisperTube MLX")
        url = gr.Textbox(label="YouTube URL", placeholder="https://www.youtube.com/watch?v=...")
        transcribe = gr.Button("Transcribe", variant="primary")
        status = gr.Textbox(label="Status", value="Idle", interactive=False)
        preview = gr.Markdown(label="Transcript preview", value="")
        download = gr.File(label="Download Markdown", interactive=False)

        started = transcribe.click(
            fn=_begin_component_values,
            inputs=None,
            outputs=[status, preview, download, transcribe],
            queue=False,
            show_progress="hidden",
            api_visibility="private",
        )
        started.then(
            fn=terminal_handler,
            inputs=[url],
            outputs=[status, preview, download, transcribe],
            trigger_mode="once",
            concurrency_limit=1,
            show_progress="full",
            api_visibility="private",
        )

    app.queue(api_open=False, default_concurrency_limit=1)
    return app


if __name__ == "__main__":
    raise SystemExit(main())
