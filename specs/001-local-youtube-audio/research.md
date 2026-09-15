# Research: Local YouTube Audio Acquisition

## Decision 1: Use the local yt-dlp command through an argument list

- **Decision**: Invoke the locally installed `yt-dlp` executable with a structured argv list, not a
  shell command string.
- **Rationale**: It keeps URL and output-template values separated from shell parsing, is directly
  testable, and preserves the local-first architecture.
- **Alternatives considered**: Calling a hosted downloader was rejected by the constitution and
  product specification. A shell string was rejected because it adds quoting and injection risk.

## Decision 2: Force one requested video

- **Decision**: Include `--no-playlist` and pass only the normalized canonical video URL.
- **Rationale**: v0.1 explicitly treats playlist-bearing URLs as a request for the current video,
  not a playlist batch.
- **Evidence**: The [yt-dlp README](https://github.com/yt-dlp/yt-dlp/blob/master/README.md) documents
  `--no-playlist` as the single-video control.
- **Alternatives considered**: Allowing yt-dlp's default playlist behavior would violate FR-002 and
  create unrequested batch work.

## Decision 3: Select best available audio without conversion in v0.1

- **Decision**: Use `bestaudio` and preserve the source container extension in the output
  template.
- **Rationale**: This acquires audio with no additional post-processing dependency. Conversion or
  normalization can be evaluated when the transcription stage defines its input contract.
- **Evidence**: The [yt-dlp README](https://github.com/yt-dlp/yt-dlp/blob/master/README.md) documents
  `bestaudio` format selection and notes that merging formats requires ffmpeg; v0.1 does not merge.
- **Alternatives considered**: Forcing MP3 or another fixed format would add conversion behavior
  and a dependency before the transcription input contract is known.

## Decision 4: Read browser cookies only through yt-dlp's local browser integration

- **Decision**: Make `--cookies-from-browser BROWSER` an explicit optional retry path. Never add a
  cookie-file export option.
- **Rationale**: Browser session data remains on the Mac and is not copied into the repository.
- **Evidence**: The [yt-dlp README](https://github.com/yt-dlp/yt-dlp/blob/master/README.md) documents
  supported browser sources for `--cookies-from-browser`.
- **Alternatives considered**: A checked-in or repository-local `cookies.txt` file was rejected as
  a credential-leak risk and is prohibited by the constitution.

## Decision 5: Keep deterministic tests in the Python standard library

- **Decision**: Use `unittest` for URL, validation, and command-construction tests; reserve the
  live YouTube request for a local smoke test.
- **Rationale**: The repository has no dependency-management configuration yet, and CI must remain
  deterministic and independent of network access, browser credentials, private media, and Apple
  Silicon hardware.
- **Alternatives considered**: A live YouTube request in CI was rejected because source availability
  and anti-bot behavior are unstable and could expose credentials.

## Open questions resolved

No unresolved technical or product questions remain for this v0.1 plan. Whisper package selection,
audio conversion, and end-to-end transcript handling belong to later milestones.
