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

## Not yet verified

- Whether `yt-dlp` is installed and callable on the maintainer's Mac for this project.
- Whether `ffmpeg` is installed and callable.
- Whether anonymous local `yt-dlp` can download the current test video.
- Whether `--cookies-from-browser safari` is needed or works on the maintainer's machine.
- No application code exists yet for URL normalization or downloading.
- MLX Whisper has not yet been selected/verified in this repository.

## Current blocker

No code blocker yet. The next step is a minimal local capability check for YouTube audio acquisition on the maintainer's actual Mac.

## Next task

Implement the smallest v0.1 foundation that can be reviewed without pretending to have access to the maintainer's browser/network:

1. add a small Python module/CLI for single-video URL normalization and yt-dlp command construction;
2. add unit tests for normal watch URLs, `youtu.be`, Shorts, and watch URLs containing playlist parameters;
3. keep the actual live YouTube download as maintainer-local verification;
4. document one exact local command for the maintainer to run against the test video.

Do **not** add Whisper or a GUI yet.

## Test video

`https://www.youtube.com/watch?v=gmj41fQTbfY`

## Maintainer-local verification target

When Codex finishes the next task, it should provide one command that attempts a real local download of the test video's best audio into an ignored temp directory.

Expected success evidence:

- yt-dlp reaches `[download] 100%`;
- an audio file exists under the ignored local temp directory;
- no cookie/session file is written into the repository.
