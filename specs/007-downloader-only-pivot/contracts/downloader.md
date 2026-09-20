# Downloader-Only Contract

## Product boundary

Input:
- one explicit YouTube video URL; or
- one explicit YouTube playlist URL.

Output:
- downloaded best-available audio file(s) under a predictable local folder.

No transcription occurs.

## URL dispatch

| Input URL | Behavior |
| --- | --- |
| Explicit watch / youtu.be / Shorts / live / embed URL | One video only |
| Explicit `/playlist?list=...` URL | Full playlist |
| Watch URL containing `list=` | One video only |

## yt-dlp behavior

Single video:
- best audio;
- no playlist traversal.

Playlist:
- playlist traversal enabled;
- preserve playlist order in filename;
- continue past individual unavailable entries when supported.

## Output

Default root:

`~/Downloads/WhisperTube/`

Single-video template:

`%(title)s [%(id)s].%(ext)s`

Playlist template:

`%(playlist)s/%(playlist_index)03d - %(title)s [%(id)s].%(ext)s`

No MP3 conversion.

## Forbidden runtime dependencies

Normal workflow must not require or invoke:

- mlx-whisper
- MLX
- OpenCC
- Gradio
- local HTTP server
- transcription pipeline
- Colab upload/API integration
