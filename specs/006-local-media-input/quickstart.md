# Quickstart: Local Audio Input

## Prerequisites

- Native Apple Silicon Mac with the v1.0 environment installed.
- Existing `.venv` with pinned Gradio, MLX Whisper, OpenCC, and ffmpeg available on PATH.
- A non-sensitive local audio fixture outside tracked source, using one of: `.aac`, `.flac`, `.m4a`, `.mp3`, `.ogg`, `.wav`, `.webm`.

## Deterministic validation

```bash
python3 -m unittest tests.test_gui tests.test_transcription -v
python3 -m unittest discover -s tests -v
```

Expected result: local-only dispatch calls `transcribe_audio()` without yt-dlp, URL behavior still calls `run_pipeline()`, neither/both input cases call no backend, and the original fixture remains byte-identical after success and injected failures.

## Local GUI smoke

```bash
./scripts/launch_macos.sh --model mlx-community/whisper-tiny --audio-dir temp/v1-1-local-audio-smoke-audio --output-dir temp/v1-1-local-audio-smoke-transcripts
```

In the loopback browser UI, choose the non-sensitive local audio fixture, leave the YouTube URL empty, and press **Transcribe**. Record only:

- suffix used and explicit model;
- non-empty Markdown success;
- original fixture still exists with unchanged bytes;
- no yt-dlp acquisition or public share URL;
- loopback-only GUI behavior.

Do not commit the fixture, audio content, transcript content, model cache, or absolute local paths.

## Out-of-scope check

Do not use `.mp4`, `.mov`, or `.mkv` for this feature; local video input is intentionally unsupported.
