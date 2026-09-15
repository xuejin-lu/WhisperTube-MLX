# Project Status

## Current milestone

**v0.1 — Local YouTube audio acquisition**

## Verified

- Public GitHub repository exists: `xuejin-lu/WhisperTube-MLX`.
- Repository currently has a Python `.gitignore`, MIT license, README, and project workflow/spec files.
- Local clone exists on the maintainer's Mac under:
  `~/Developer/xuejin-lu/WhisperTube-MLX`
- Git working tree was clean immediately after cloning.
- The project decision is to run YouTube acquisition locally on the Mac rather than from Colab/datacenter IPs.
- The repository ignores cookies, local media, temp/output folders, and common model/cache artifacts.
- Single-video URL normalization is implemented for watch URLs, `youtu.be`, Shorts, and playlist-bearing watch URLs.
- The local CLI builds a `yt-dlp --no-playlist --format bestaudio/best` command and supports `--cookies-from-browser`.
- Unit tests cover URL normalization and command construction without requiring a live YouTube request.

## Not yet verified

- Whether `yt-dlp` is installed and callable on the maintainer's Mac for this project.
- Whether anonymous local `yt-dlp` can download the current test video.
- Whether `--cookies-from-browser safari` is needed or works on the maintainer's machine.
- MLX Whisper has not yet been selected/verified in this repository.

## Current blocker

No code blocker. Live YouTube download and browser-cookie behavior require verification on the maintainer's actual Mac.

## Next task

Run the documented maintainer-local `yt-dlp` command against the test video and record whether anonymous access succeeds or the Safari cookie fallback is required.

Do **not** add Whisper or a GUI yet.

## Test video

`https://www.youtube.com/watch?v=gmj41fQTbfY`

## Maintainer-local verification target

When Codex finishes the next task, it should provide one command that attempts a real local download of the test video's best audio into an ignored temp directory.

Expected success evidence:

- yt-dlp reaches `[download] 100%`;
- an audio file exists under the ignored local temp directory;
- no cookie/session file is written into the repository.
