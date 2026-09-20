# Data Model: Local Audio Input

## RequestSelection

Represents the two GUI input values for one Transcribe request.

| Field | Type | Rules |
| --- | --- | --- |
| `youtube_url` | `str` or empty | Trimmed before validation; mutually exclusive with `local_audio_path`. |
| `local_audio_path` | `str`/`Path` or empty | One framework-managed filepath; validated by the canonical transcription boundary. |
| `model` | `str` | Defaults to `mlx-community/whisper-large-v3-mlx`; explicit tiny override remains supported. |
| `output_dir` | `str`/`Path` | Approved ignored runtime root; existing GUI output validation applies. |

### Valid states

- URL only: dispatch to `run_pipeline()`.
- Local audio only: dispatch to `transcribe_audio()`.

### Invalid states

- Neither input: input error; no backend call.
- Both inputs: input error asking the user to choose exactly one; no backend call.

## LocalAudioSource

The selected source filepath is user-owned input. It may be a browser/Gradio framework-managed copy during the local loopback request, but the original file remains outside app-owned cleanup.

Validation is delegated to `transcribe_audio()`:

- regular readable file;
- suffix in `.aac`, `.flac`, `.m4a`, `.mp3`, `.ogg`, `.wav`, `.webm`;
- no local video containers;
- never mutated by the GUI route.

## TranscriptArtifact

The existing generated Markdown artifact remains the output entity:

- app-generated under an approved ignored runtime root;
- non-empty UTF-8 Markdown;
- validated before preview/download;
- same bytes in preview and download;
- existing stem collision is an explicit output error, never silent overwrite.

## Ownership transitions

```text
User-owned local source --read-only--> local transcription
YouTube URL --run_pipeline--> app-owned temporary audio --existing cleanup--> transcript artifact
local transcription / YouTube transcription --> validated transcript artifact --> controlled GUI cache/download
```
