# Project Status

## Current milestone

**v0.2 — Local MLX transcription**

## v0.1 approval

**APPROVED on 2026-09-16.**

v0.1 Local YouTube audio acquisition is closed after reviewer verification of:

- Spec Kit convergence complete with 25/25 tasks checked;
- security checklist 12/12 and requirements checklist 16/16 reviewed;
- deterministic regression coverage for URL handling, CLI failures, output-path traversal, privacy contract, and downloader command construction;
- strict `yt-dlp --format bestaudio` contract aligned with FR-003;
- relative output traversal such as `temp/../../outside` rejected before downloader invocation;
- anonymous local yt-dlp smoke test succeeded on the development Mac with format `251` and an ignored `.webm` artifact;
- no cookie export or credential file was produced;
- GitHub Actions passed for commit `9c68ccd` in run `35021028881`.

The Safari/browser-cookie fallback remains intentionally unexercised because anonymous acquisition succeeded. This is a dormant fallback risk, not a v0.1 blocker.

## v0.2 verification

- v0.2 Spec Kit artifacts are complete under `specs/002-mlx-transcription/`: spec, plan, research,
  data model, CLI contract, quickstart, checklists, and ordered tasks.
- The agent reviewer checked all requirements/security checklist items after resolving one absolute
  output-path wording inconsistency and one missing paragraph-formatting requirement.
- Local Apple Silicon dependencies installed successfully: `mlx-whisper 0.4.3`, `mlx 0.32.2`, and
  `OpenCC 1.4.2`.
- Real local MLX smoke succeeded on `arm64` using `mlx-community/whisper-tiny` against the v0.1
  audio artifact. It produced one 33 KiB UTF-8 Markdown transcript under
  `temp/transcripts-v0-2-timed/` in 42.97 seconds, with recognizable Chinese text and no human gate.
- Deterministic tests use injected backend/converter fakes; no audio or transcript content is sent
  to a hosted service.
- The full deterministic suite passes with 30 tests, including the unchanged v0.1 acquisition tests;
  `compileall` and `git diff --check` also pass.
- GitHub Actions run `35032658795` passed for pushed commit `d55aece`.

## Review findings

v0.2 is **not yet approved for closure**. Repository review found three deterministic/spec-alignment gaps:

1. **Paragraphs are hard-sliced, not natural/readable**: `format_paragraphs()` collapses whitespace and slices every 500 code points. This can split a sentence in the middle even though FR-005 and the project-level output requirement call for readable paragraphs targeting roughly 500 Chinese characters. Paragraph formation should prefer sentence/punctuation boundaries and only hard-split when no reasonable boundary exists.
2. **Backend error classification can mislabel audio/dependency failures as model failures**: `transcribe_audio()` currently maps backend `FileNotFoundError`, `IsADirectoryError`, `KeyError`, and `ValueError` to `ModelError`. MLX Whisper audio decoding depends on local ffmpeg; a missing decoder or malformed/undecodable audio can therefore be reported as "unable to load model". v0.2 requires cause-specific dependency/model/inference handling. Add a deterministic preflight/error boundary so missing ffmpeg is a dependency error and audio decode/inference failures are not mislabeled as model errors.
3. **OpenCC configuration drift**: the project-level specification names OpenCC `s2tw` (or a documented equivalent) and requires no semantic rewriting, while the implementation selects `s2twp`, which additionally performs Taiwan regional phrase conversion. Unless the feature spec intentionally and explicitly changes this product decision, use `s2tw` for the v0.2 baseline and test the selected configuration.

## Current milestone goal

v0.2 must establish a local Apple Silicon transcription path:

`local audio file -> MLX-compatible Whisper -> Chinese transcript`

Do **not** connect the YouTube downloader to transcription yet. End-to-end composition belongs to v0.3.

## Current blocker

The three review findings above block v0.2 approval. They are deterministic and should be resolved autonomously through Spec Kit convergence and TDD; no maintainer shell work or human authorization is required.

## Next autonomous task

Run a v0.2 Spec Kit convergence pass for the three review findings above, then implement the corrective tasks with RED -> GREEN -> REFACTOR:

- add sentence-aware / punctuation-aware paragraph-formatting tests around the ~500-character target while preserving transcript content;
- replace fixed hard slicing with natural-boundary paragraph grouping, retaining a safe hard-split fallback for pathological long spans;
- add deterministic error-boundary tests for missing ffmpeg/audio decode failure versus model/inference failure, then fix cause-specific classification;
- reconcile OpenCC `s2tw` versus `s2twp` with the top-level project spec; absent an explicit product-spec change, use and test `s2tw`;
- run focused tests, the full deterministic suite, local Apple Silicon smoke validation, CI, and `$speckit-converge`;
- push and request review again.

Do **not** start v0.3 until v0.2 is approved.

## Constraints carried forward

- Local-first and privacy-first.
- Apple Silicon Mac is the initial target.
- Free/open tooling preferred.
- No hosted transcription API.
- No GUI yet.
- No summarization, diarization, or word-level timestamps in v0.2.
- Do not modify the proven v0.1 acquisition behavior unless a v0.2 integration need exposes a real defect; if so, create a separate convergence/fix task.

## Known follow-up risks

- Safari browser-cookie fallback has not been exercised because it was not needed during v0.1 verification.
- yt-dlp emitted a missing JavaScript-runtime warning during v0.1 smoke verification, although the tested video downloaded successfully.
- The default large-v3 model remains a quality target; the local smoke used tiny to avoid a multi-GB model download during routine validation.
