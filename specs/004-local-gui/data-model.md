# Data Model: Local Graphical UI

## GUIRequest

- `url`: trimmed non-empty single-video URL submitted by the user
- `model`: launch-time model identifier; defaults to the approved large-v3 target
- `audio_dir`: approved ignored pipeline audio root
- `output_dir`: approved ignored transcript root

Validation: blank URL is rejected before the pipeline. Pipeline URL validation remains authoritative.

## GUIStatus

Values: `idle`, `running`, `success`, `error`.

Transitions:

```text
idle -> running -> success
idle -> running -> error
success/error -> running -> success/error
```

Entering `running` clears stale preview and download state.

## GUIResult

- `status`: terminal `success` or `error`
- `message`: safe user-facing status text containing an approved category when applicable
- `preview`: complete Markdown text only on success
- `transcript_path`: validated transcript artifact only on success

## TranscriptArtifact

- resolved regular file below the configured transcript root
- `.md` suffix
- non-empty, readable UTF-8 content
- retained by the pipeline and never deleted by the GUI

## GUILaunchConfig

- loopback host `127.0.0.1`
- public sharing disabled
- analytics disabled
- monitoring disabled
- strict CORS enabled
- one active queued event
- no transcript directory or parent is added to framework `allowed_paths`
- ambient `GRADIO_ALLOWED_PATHS` overrides are rejected
- only a validated transcript copied into Gradio's controlled cache is downloadable
