# Research: Local Graphical UI

## Decision 1: Use Gradio 6.27.0 Blocks

**Decision**: Pin `gradio==6.27.0` in a dedicated UI requirements file and build one Blocks app.

**Rationale**: Current official Gradio documentation provides native text input, button events, queued
long-running work, Markdown output, file download, local launch, and explicit privacy controls. It wraps
the existing Python pipeline directly and is Apache-2.0 licensed.

**Alternatives considered**:

- Streamlit provides status and download widgets plus AppTest, but its script rerun/session model adds
  state-management complexity around one long-running injected pipeline call.
- Tkinter ships with many Python distributions and has no local web server, but Markdown preview,
  download/save UX, background work, and testing would require significantly more custom code.

## Decision 2: Make local-only/privacy settings explicit

**Decision**: Construct Blocks with `analytics_enabled=False`; launch with `server_name="127.0.0.1"`,
`share=False`, `enable_monitoring=False`, `strict_cors=True`, and `show_error=False`; queue with one worker
and closed direct API access.

**Rationale**: Gradio defaults analytics to enabled and monitoring to available, while environment variables
can affect sharing or binding. Explicit values preserve the constitution regardless of ambient configuration.

**Alternatives considered**: Relying on framework defaults was rejected because defaults and environment
variables can change or enable behavior outside the local-only contract.

## Decision 3: Separate pure result adaptation from components

**Decision**: A framework-independent handler validates the trimmed URL, calls an injected pipeline, validates
the returned transcript below the approved root, reads UTF-8 Markdown, and returns a typed result. Thin adapter
functions translate typed states to Gradio component values.

**Rationale**: Pure tests can cover all failure categories, stale-output clearing, exact preview bytes, and path
security without a browser, YouTube, models, or Apple Silicon. A smaller construction test verifies the pinned
Gradio API and launch contract.

**Alternatives considered**: Embedding all logic in a button callback was rejected because it couples product
behavior to framework objects and weakens deterministic testing.

## Decision 4: Bound file serving to validated transcripts

**Decision**: Return a file output only after validating a non-empty regular `.md` file under the configured
transcript root. Do not add the transcript root to `allowed_paths`; let pinned Gradio copy the validated result
into its controlled cache, and reject ambient `GRADIO_ALLOWED_PATHS` overrides.

**Rationale**: Official Gradio file-access guidance states that a directory in `allowed_paths` exposes every file
under it, while a callback-returned file in the system temp directory is copied into Gradio's cache. Avoiding the
directory allowlist preserves v0.3 output boundaries while keeping the validated result downloadable.

**Alternatives considered**: Serving the transcript root, arbitrary paths, or broad repository directories was
rejected as an unnecessary local-file disclosure risk. An exact launch-time artifact allowlist is unavailable
because the result does not exist until after the callback completes.
