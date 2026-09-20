# Local Audio GUI Contract

## Dispatch

Exactly one input route per run:

| YouTube URL | Local audio | Result |
| --- | --- | --- |
| present | absent | existing YouTube pipeline |
| absent | present | local transcription |
| absent | absent | input error; no backend call |
| present | present | input error; no backend call |

## Ownership

- YouTube current-run audio: app-owned temporary data; existing cleanup contract applies.
- User-selected local audio: user-owned; never delete/move/rename/overwrite.
- Framework upload/cache copy: framework-owned temporary data only; never broaden file serving to the source directory.
- Transcript: app-generated output under approved runtime output root.

## Supported local audio suffixes

`.aac`, `.flac`, `.m4a`, `.mp3`, `.ogg`, `.wav`, `.webm`.

Local video containers are outside this feature.

## Security invariants

- loopback only;
- no public share/tunnel;
- no telemetry/hosted processing;
- no broad `allowed_paths`;
- reject ambient `GRADIO_ALLOWED_PATHS`;
- only validated Markdown result may be exposed for download;
- browser-visible unexpected errors remain sanitized.
