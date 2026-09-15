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
- Spec Kit v1.0.3 is bootstrapped with a constitution and the v0.1 feature artifacts under `specs/001-local-youtube-audio/`.
- The reviewer-owned security checklist has 12/12 requirements-quality items reviewed and checked.
- Local `yt-dlp 2026.08.19` and `ffmpeg 9.0.1` are callable on the development Mac.
- Anonymous smoke acquisition of the test video succeeded with `[download] 100%` and created one ignored `.webm` file under `temp/audio/`.
- No cookie export or repository credential file was created; the browser-cookie fallback was not needed for this successful anonymous run.

## Not yet verified

- Whether `--cookies-from-browser safari` is needed or works on the maintainer's machine.
- MLX Whisper has not yet been selected/verified in this repository.
- Whether a JavaScript runtime is needed for future YouTube videos or formats; the current smoke run emitted a yt-dlp warning but succeeded.

## Current blocker

No v0.1 code blocker. Safari cookie behavior remains unexercised because anonymous access succeeded;
the current yt-dlp JavaScript-runtime warning is a follow-up risk for future videos or formats.

## Next task

Review the converged v0.1 implementation and decide whether to approve transition to v0.2 MLX transcription.

Do **not** add Whisper or a GUI yet.

## Test video

`https://www.youtube.com/watch?v=gmj41fQTbfY`

## Maintainer-local verification target

When Codex finishes the next task, it should provide one command that attempts a real local download of the test video's best audio into an ignored temp directory.

Expected success evidence:

- yt-dlp reaches `[download] 100%`;
- an audio file exists under the ignored local temp directory;
- no cookie/session file is written into the repository.
