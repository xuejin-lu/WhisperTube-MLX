# Data Model: Downloader-Only Pivot

## DownloadRequest

An immutable request derived from one user URL.

| Field | Type | Rules |
|---|---|---|
| `kind` | `RequestKind` | `VIDEO` or `PLAYLIST` |
| `url` | `str` | trimmed HTTPS/HTTP YouTube URL; video requests are canonicalized |
| `video_id` | `str \| None` | exactly 11 YouTube ID characters for video requests |
| `output_root` | `Path` | defaults to `~/Downloads/WhisperTube/`; injectable for tests |
| `cookies_from_browser` | `str \| None` | only populated by an explicit CLI flag |

## RequestKind

- `VIDEO`: one video, always passed to yt-dlp with `--no-playlist`.
- `PLAYLIST`: explicit `/playlist?list=...`, passed with `--yes-playlist` and
  `--ignore-errors`.

## Output templates

- Video: `%(title)s [%(id)s].%(ext)s` below `output_root`.
- Playlist: `%(playlist)s/%(playlist_index)03d - %(title)s [%(id)s].%(ext)s`
  below `output_root`.

yt-dlp owns filename sanitization and extension selection. The Python wrapper does
not rename or convert downloaded files.

## DownloadSummary

The runner reports:

- `downloaded`: number of yt-dlp `after_move` completion markers observed;
- `failed_or_skipped`: number of error lines observed, or one fallback failure for
  a non-zero process exit with no explicit error line;
- `output_root`: the configured destination;
- `returncode`: yt-dlp's process exit code.

The summary is informational; the process return code remains authoritative for
single-video failure and unexpected process failure.
