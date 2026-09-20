# Research: Downloader-Only Pivot

## Decision: keep the wrapper standard-library-only

The active Python layer will use `argparse`, `dataclasses`, `pathlib`,
`subprocess`, and `urllib.parse`. The only installed project dependency is the
pinned `yt-dlp` executable. This removes MLX Whisper, OpenCC, and Gradio from the
normal setup and keeps CI deterministic without Apple Silicon packages.

Rationale: the product no longer transcribes or serves a web UI. A thin wrapper is
enough to classify URLs, construct safe argv, stream progress, and summarize the
yt-dlp result.

Alternative considered: retaining the existing GUI/pipeline stack would preserve a
second competing workflow and violate the explicit out-of-scope requirements.

## Decision: classify explicit playlists before video normalization

An explicit `youtube.com/playlist?list=...` URL is a playlist request. A watch URL
with `list=` is always normalized as one video and receives `--no-playlist`.
The existing video ID validation and supported watch/shorts/live/embed/short-link
forms remain the single-video parser contract.

Rationale: this directly encodes the product's safety boundary and avoids
accidentally downloading a playlist from a copied watch URL.

## Decision: delegate playlist continuation to yt-dlp

Playlist commands use `--yes-playlist`, `--ignore-errors`, `--newline`, and an
`after_move` print marker. The runner streams yt-dlp output and counts completion
markers plus error lines for the final summary instead of reimplementing playlist
traversal.

Rationale: yt-dlp owns extraction, unavailable-entry handling, and format selection;
the wrapper should only add predictable naming and user-facing reporting.

## Decision: use bestaudio without post-processing

Both request types pass `--format bestaudio` and no `--extract-audio`, codec, or MP3
postprocessor options. The output template preserves yt-dlp's selected source
extension (`.webm`, `.m4a`, or another best-audio extension).

## Decision: default to a user Downloads directory

The default root is computed as `Path.home() / "Downloads" / "WhisperTube"` at
runtime. Tests and smoke runs may inject an absolute temporary root. The wrapper
creates the root when needed and never deletes existing user files.

## Decision: make browser cookies explicit

`--cookies-from-browser BROWSER` is appended only when the user explicitly passes
the option. The wrapper never exports or writes cookies and never opens a browser.

## Decision: delete obsolete active modules, preserve historical access

The current mainline will remove the GUI, pipeline, transcription, release
diagnostic, and old product tests from the active source tree. The v1.0.0 tag and
Git history preserve them for historical access. This prevents stale setup and
README paths from advertising unsupported transcription behavior.
