# Project Status

## Current milestone

**v1.1 candidate — Local audio input**

## v0.1 approval

**APPROVED on 2026-09-16.**

v0.1 Local YouTube audio acquisition is closed after reviewer verification of:

- Spec Kit convergence complete with 25/25 tasks checked;
- security checklist 12/12 and requirements checklist 16/16 reviewed;
- deterministic regression coverage for URL handling, CLI failures, output-path traversal, privacy contract, and downloader command construction;
- strict `yt-dlp --format bestaudio` contract aligned with FR-003;
- relative output traversal such as `temp/../../outside` rejected before downloader invocation;
- anonymous local yt-dlp smoke test succeeded with format 251 and an ignored `.webm` artifact;
- no cookie export or repository credential file was created;
- GitHub Actions passed for commit `9c68ccd` in run `35021028881`.

## v0.2 approval

**APPROVED on 2026-09-16.**

v0.2 Local MLX transcription is closed after reviewer verification of:

- Spec Kit convergence complete with T001-T030 checked;
- requirements checklist 8/8 and security checklist 9/9 reviewed;
- focused transcription tests expanded to 21 and the full repository suite to 36;
- paragraph formatting prefers sentence/punctuation boundaries near the ~500-character target and preserves content;
- ffmpeg/dependency, model, and audio-decode/inference failures are cause-specific;
- OpenCC uses the project baseline `s2tw`;
- Apple Silicon MLX smoke succeeded with `mlx-community/whisper-tiny`;
- GitHub Actions passed for commit `9caff16` in run `35047914567`.

The default `mlx-community/whisper-large-v3-mlx` remains the quality target; a full large-v3 smoke is still a later performance/compatibility check rather than a v0.2 closure requirement.

## v0.3 approval

**APPROVED on 2026-09-19.**

v0.3 End-to-end CLI pipeline is closed after reviewer verification of:

- Spec Kit convergence complete through T018;
- requirements and security checklists reviewed;
- one command composes the approved v0.1 acquisition and v0.2 transcription stages without duplicating their logic;
- temporary current-run audio is cleaned after success and transcription failure while the transcript is retained;
- cleanup never extends to arbitrary/pre-existing paths;
- simultaneous transcription failure + cleanup failure preserves the original stage category/exit code and also reports residual-audio risk;
- the default acquirer removes partial artifacts only from its dedicated current-run `run-*` directory after acquisition failure;
- focused pipeline suite passes 10 tests and the full deterministic suite passes 46 tests;
- a post-review real Apple Silicon smoke with the approved public video and `mlx-community/whisper-tiny` produced a local Markdown transcript and left the pipeline audio directory empty;
- GitHub Actions passed for remediation commit `434c0c0` in run `35402460908`;
- GitHub Actions passed for final verification commit `2d972ef` in run `35402516879`.

No v0.3 implementation blocker or Human Gate remains.

## v0.4 approval

**APPROVED on 2026-09-19.**

v0.4 Local Graphical UI is closed after reviewer verification of:

- Spec Kit convergence complete through T022;
- requirements checklist 13/13, security checklist 10/10, and UX checklist 10/10 reviewed;
- a pinned Gradio 6.27.0 Blocks interface delegates one request to the approved v0.3 pipeline;
- loopback-only binding, no public share, private event APIs, strict CORS, disabled analytics/monitoring, and one-active-job behavior are enforced;
- visible idle/running/success/error states, cause-specific pipeline errors, full Markdown preview, and local download are implemented;
- transcript results are validated for root, suffix, file type, readability, UTF-8, and non-empty content before GUI exposure;
- the broad transcript-directory `allowed_paths` exposure was removed;
- ambient `GRADIO_ALLOWED_PATHS` is rejected so environment configuration cannot silently re-enable broad file serving;
- pinned-Gradio integration tests prove an unrelated pre-existing transcript-root file returns HTTP 403 while the validated Markdown result is served from Gradio's controlled cache with HTTP 200 and byte-identical content;
- focused GUI tests pass 12/12 and the full deterministic suite passes 58/58;
- a real local browser smoke produced, previewed, and downloaded the validated transcript, denied the unrelated file route, showed no public share URL, and left the current-run audio directory empty;
- GitHub Actions passed for remediation commit `44371d6` in run `35420386201`;
- GitHub Actions passed for final handoff commit `03fb16d` in run `35420473704`.

No v0.4 implementation blocker or Human Gate remains.

## Current milestone goal

v1.0 turns the approved local pipeline and GUI into a public, reasonably installable release for other Apple Silicon Mac users.

The target user journey is:

`obtain release -> install/setup prerequisites -> launch locally -> paste URL -> Transcribe -> save Markdown`

The release must preserve all approved v0.1-v0.4 privacy, cleanup, error, and local-file boundaries.

## Next autonomous task

Use the Spec Kit lifecycle to create the v1.0 **Public Usable Release** feature before implementation.

Codex should autonomously:

1. research the simplest maintainable installation/distribution approach for Apple Silicon macOS rather than assuming a packaging tool;
2. decide through the spec whether v1.0 should ship as:
   - a reproducible setup/launch script,
   - a packaged macOS app,
   - or both;
3. explicitly account for Python/runtime dependencies, `yt-dlp`, `ffmpeg`, MLX/Whisper/OpenCC, Gradio, model download/cache behavior, and Apple Silicon compatibility;
4. define acceptance criteria for a clean-machine or clean-environment installation path, launch path, uninstall/cleanup expectations, and troubleshooting;
5. keep all processing local and preserve the approved loopback-only GUI and file-serving boundaries;
6. add release/version metadata and a versioned GitHub Release plan without publishing a release before acceptance criteria converge;
7. improve README/setup/troubleshooting so another Apple Silicon Mac user can follow it without repository-specific knowledge;
8. add deterministic installer/launcher/config tests where practical and keep CI independent of Apple Silicon-only MLX execution;
9. perform real Apple Silicon release-path smoke verification using the approved public test video and an explicit small MLX model;
10. inspect the repository/release artifacts for credentials, media, private transcripts, model caches, and accidental local paths before publication;
11. run full tests, CI, `$speckit-converge`, push, and persist the review handoff in GitHub;
12. do **not** create/publish the actual GitHub Release until the v1.0 release candidate is explicitly approved by repository review.

## v1.0 scope constraints

- Apple Silicon macOS only for the initial public release.
- No hosted transcription, public tunnel, paid API fallback, accounts, database, or telemetry.
- No playlist batch transcription, summarization, diarization, or timestamps.
- Do not weaken the approved v0.1-v0.4 pipeline, cleanup, privacy, error, or file-serving contracts.
- Preserve `large-v3` as the normal quality target while allowing a smaller explicit model for validation.
- Prefer the smallest distribution approach that is reproducible and understandable over packaging complexity for its own sake.
- Release publication is a separate final approval action, not an automatic consequence of code completion.

## v1.0 implementation state

**Candidate version**: `1.0.0` — implementation complete; repository review pending; GitHub Release not published.

The pre-implementation Agent Reviewer Phase is complete for `specs/005-public-usable-release/`:

- requirements checklist: 13/13 reviewed;
- security checklist: 15/15 reviewed;
- CHK012 requirements defect was fixed before marking it `[x]`: browser login/cookie, Keychain, and macOS privacy prompts are explicit user-owned gates that release paths must not bypass or capture;
- migration artifacts were protected in commit `ff94b9d` (`docs: define v1.0 public release workflow`) and rebased onto `origin/main`.

Verified locally so far:

- native Apple Silicon prerequisite diagnostic passes with Python 3.13, macOS 14+, `ffmpeg`, and `yt-dlp`;
- setup completed from the new script and a second setup run reused all pinned dependencies without destructive cleanup;
- deterministic release-focused tests pass 12/12;
- the full deterministic suite passes 70/70 under the v1.0 environment;
- the launcher served the GUI at `127.0.0.1` with HTTP 200 and was stopped cleanly without a public share URL;
- the approved public test video completed with explicit `mlx-community/whisper-tiny`, producing a 33,924-byte UTF-8 Markdown transcript and leaving the current-run audio directory empty;
- artifact inspection found no tracked private/runtime artifact; the smoke transcript and audio remain under ignored `temp/` paths.

Risks and final publication gate:

- Spec Kit converge is complete with no remaining tasks appended;
- staged candidate artifact inspection is clean, and deterministic CI passed for implementation commit `a165701` in GitHub Actions run `35436400122`;
- keep full large-v3 performance unmeasured, Safari cookie fallback unexercised, and the yt-dlp JavaScript-runtime warning documented as risks;
- do not publish the actual GitHub Release until repository review explicitly approves the candidate.

**Review state**: v1.0 implementation is pushed and ready for repository review. The remaining action is review approval before creating the actual GitHub Release.

## Spec Kit convergence

**CONVERGED on 2026-09-19.**

The v1.0 implementation satisfies the active spec, plan, tasks, and constitution within the selected source-release scope. No convergence tasks were appended. The remaining items are review/publication gates or explicitly documented risks, not unbuilt feature work.

## Known follow-up risks

- Safari browser-cookie fallback remains unexercised because anonymous YouTube acquisition has succeeded in testing.
- yt-dlp has emitted a missing JavaScript-runtime warning on tested downloads, although the approved test video succeeds.
- full large-v3 runtime cost and memory use remain unmeasured.
- Gradio is pinned at 6.27.0; future framework upgrades require rerunning the launch/privacy contract tests and browser smoke.
- macOS distribution/signing/notarization requirements have not yet been selected; v1.0 research must determine whether they are necessary for the chosen distribution path.


## v1.0 repository review findings

**NOT APPROVED FOR PUBLICATION — remediation required.**

Repository review found one clean-machine runtime blocker and one corresponding test-coverage gap:

1. **The documented launcher does not expose the project-installed `yt-dlp` executable to the pipeline.**
   `scripts/setup_macos.sh` installs pinned `yt-dlp` into `.venv/bin/yt-dlp`, but
   `scripts/launch_macos.sh` executes `.venv/bin/python -m whispertube.gui` without activating the
   environment or prepending `.venv/bin` to `PATH`. The approved downloader invokes `yt-dlp` by
   executable name through `subprocess.run()`. On a clean user Mac with no global `yt-dlp`, the GUI
   can therefore fail at first acquisition even though setup successfully installed the dependency.
   The development-machine smoke can miss this because a global `yt-dlp` may already be present.
2. **The release test evidence does not currently exercise this shell/runtime boundary.**
   T010 is marked complete, but `tests/test_release.py` currently checks script text rather than executing
   a clean-PATH launcher/setup scenario that proves the project-owned `yt-dlp` is the one available at runtime.

The release list is still empty, so no premature GitHub Release publication occurred. Both release scripts are
tracked executable (`100755`), and latest candidate CI is green; those facts do not remove the clean-PATH blocker.

## v1.0 current blocker

The clean-path blocker described above was resolved in the working tree by explicitly prepending the project
`.venv/bin` to `PATH` in `scripts/launch_macos.sh`. It remains a repository-review finding until the remediation
commit is pushed and independently reviewed; the GitHub Release remains unpublished.

## v1.0 clean-path remediation

**IMPLEMENTED AND CI-VERIFIED — repository review pending.**

The focused convergence pass completed the requested remediation:

- T029 added RED runtime coverage that launches from a temporary project path with spaces, removes global `yt-dlp`
  from `PATH`, preserves launcher arguments, and proves the project-owned `.venv/bin/yt-dlp` is discoverable.
- T030 added execution coverage for setup reruns, failed native prerequisites, missing `.venv`, paths with spaces, and
  launcher argument preservation.
- T031 prepends the project `.venv/bin` to `PATH` before starting the GUI, preserving loopback-only binding and the
  no-public-share boundary.
- The four new clean-path regression tests pass 4/4 after the expected RED failure and GREEN fix; the full focused
  release module passes 11/11 and the full deterministic suite passes 74/74.
- A clean-PATH GUI verification served `http://127.0.0.1:17861/` with HTTP 200 and no public share URL.
- A real Apple Silicon clean-PATH pipeline smoke using the approved public video and
  `mlx-community/whisper-tiny` produced a 34,175-byte UTF-8 Markdown transcript and left the current-run audio
  directory empty. The PATH included the project `.venv/bin`, Homebrew `ffmpeg`, and system directories; no global
  `yt-dlp` was required.
- Remediation commit `1ddb23dce0c64998ebb6156df4c371574159cdd38` is pushed to `origin/main`; GitHub Actions run
  `35440765844` completed with `success`.
- The follow-up Spec Kit convergence pass found no remaining unbuilt work after T029-T032; T033 is complete.

The remaining action is repository review of this pushed remediation. Do not create tag `v1.0.0` or publish the
GitHub Release.

## v1.0 original implementation plan

Run a focused v1.0 Spec Kit convergence pass:

- add RED script/runtime regression coverage that creates a fake/minimal project virtual environment, removes any
  global `yt-dlp` from the test PATH, and proves the documented launcher still makes the project-owned
  `.venv/bin/yt-dlp` discoverable to the launched process;
- add/repair deterministic shell tests for the T010 claims (rerun safety, missing prerequisite behavior,
  missing `.venv`, paths with spaces, and launcher argument preservation) rather than relying only on source-text assertions;
- implement the smallest safe launcher/setup fix, preferably by explicitly prepending the project `.venv/bin`
  to `PATH` before exec or by another equally explicit project-owned executable path;
- rerun focused release tests, the full deterministic suite, clean-PATH launch verification, real Apple Silicon
  small-model release smoke, artifact inspection, exact-SHA CI, and `$speckit-converge`;
- update `docs/RELEASE.md` evidence/checklist state so completed candidate checks are distinguishable from the
  still-separate publication action;
- keep the GitHub Release unpublished and request repository review again.

Do not create tag `v1.0.0` or publish the GitHub Release until this finding is closed and the candidate is explicitly approved.


## v1.0 release-candidate approval

**APPROVED FOR PUBLICATION on 2026-09-19.**

Repository review verified the clean-path remediation and final candidate state:

- `scripts/launch_macos.sh` prepends the project `.venv/bin` to `PATH`, so the pinned project-owned `yt-dlp` is discoverable without any global yt-dlp installation;
- deterministic shell/runtime coverage exercises a clean PATH, a project path containing spaces, launcher argument preservation, missing `.venv`, failed prerequisites, and setup rerun safety;
- the four new clean-path regression tests pass 4/4, the focused release module passes 11/11, and the full deterministic suite passes 74/74;
- a clean-PATH local GUI verification served loopback-only HTTP 200 with no public share URL;
- a real Apple Silicon clean-PATH smoke using the approved public video and `mlx-community/whisper-tiny` produced a 34,175-byte UTF-8 Markdown transcript and left current-run audio empty;
- artifact/privacy inspection is complete and the release checklist is fully satisfied except for the intentionally separate publication checkbox;
- latest HEAD `5013bb4` passed GitHub Actions run `35440917903`;
- GitHub Releases are still empty and no tag exists under `refs/tags/`, so no publication occurred before approval.

No implementation blocker or Human Gate remains for the reviewed source-release candidate.

## v1.0 publication gate

The reviewed candidate is now authorized for the separate publication action, but publication has **not** been performed by repository review.

The next autonomous task, only after the maintainer starts it, is:

1. synchronize to the approved candidate state;
2. create annotated tag `v1.0.0` at the reviewed release snapshot (including this approval handoff as appropriate to the documented publication procedure);
3. create the GitHub Release using the reviewed release notes and GitHub-generated source archives only;
4. do not attach model weights, credentials, media, transcripts, cookies, browser profiles, or runtime caches;
5. verify the published tag/release points to the intended reviewed commit and that source assets are present;
6. mark the publication checkbox in `docs/RELEASE.md`, update this status with the exact tag/release URL and final verification state, commit/push any post-publication documentation update, and request one final publication verification review.

Do not add new product features during publication.

## v1.0 publication verification

**PUBLISHED on 2026-09-19 after explicit maintainer authorization.**

- Published annotated tag `v1.0.0` points to the approved release snapshot
  `b89298016a67905ad9b5685ebf79e110f8a788cb`.
- GitHub Release: https://github.com/xuejin-lu/WhisperTube-MLX/releases/tag/v1.0.0
- The Release was created as a non-draft, non-prerelease release with GitHub-generated source archives only;
  no extra assets were attached.
- `docs/RELEASE.md` publication checkbox is complete, and the repository remains free of credentials, cookies,
  browser profiles, media, transcripts, model weights, and runtime caches.
- No product features were added during publication.


## v1.0 final publication review

**PUBLICATION SUCCEEDED — metadata remediation completed; final verification closed.**

Final repository/release verification confirmed:

- annotated tag `v1.0.0` resolves to commit `b89298016a67905ad9b5685ebf79e110f8a788cb`;
- GitHub Release `v1.0.0 — Public Usable Release` is published, non-draft, non-prerelease;
- the Release has no manually attached assets; only GitHub-generated source archives are present;
- post-publication documentation commit `655cc5f` records the release and no product code changed;
- the Release body now links to the tracked `README.md` and `docs/TROUBLESHOOTING.md` at tag `v1.0.0`;
- repository wording uses the verifiable term “published annotated tag” rather than claiming GitHub tag immutability.

The previously recorded release-metadata findings are resolved:

1. The Release body now points to the tracked README and troubleshooting documentation; no nonexistent `docs/QUICKSTART.md` reference remains.
2. The status wording now says “published annotated tag”; it does not claim GitHub tag immutability.

These metadata-only corrections did not rebuild or republish v1.0.0 and do not alter the reviewed source snapshot.

## v1.0 final verification

Final publication verification is complete; no blocker remains.

## v1.0 next autonomous task

No publication task remains. Future `開始` runs should synchronize and stop unless a new feature, bug, or reviewer finding is added:

- do not create another release or version for the completed v1.0 publication;
- only begin new work when a new scoped request or reviewer finding exists.


## v1.1 local-audio-input kickoff

**IMPLEMENTATION COMPLETE — review handoff pending.**

The next scoped product feature is local audio input in the existing loopback GUI.

Repository specification:

- `specs/006-local-media-input/spec.md`
- `specs/006-local-media-input/contracts/ui.md`

The feature preserves the approved YouTube path and adds one mutually exclusive local-audio route:

`double-click launcher -> YouTube URL OR local audio -> Transcribe -> Traditional Chinese Markdown`

Hard boundaries:

- reuse the existing `transcribe_audio()` implementation rather than creating a second Whisper stack;
- initially support only the audio suffixes already accepted by the transcription module: `.aac .flac .m4a .mp3 .ogg .wav .webm`;
- local video files such as `.mp4` / `.mov` are not part of this feature;
- the user's original local audio is never cleanup-eligible and must remain unchanged on success or failure;
- URL and local-file inputs are mutually exclusive; both/neither are input errors and must not invoke a backend;
- preserve loopback-only Gradio, no public share, no broad file-serving directory, and all existing transcript validation/privacy contracts;
- no new tag or GitHub Release during implementation.

Verified implementation evidence:

- Spec Kit artifacts for feature 006 are present: plan, research, data-model, quickstart, UI contract, security checklist, and tasks.
- Agent reviewer phase completed security checklist 15/15; all requirements-quality items are traceable to the spec.
- Focused GUI/transcription suite passes 39/39; full deterministic suite passes 80/80.
- Real Apple Silicon local-audio route smoke with `mlx-community/whisper-tiny` produced a 34,456-byte UTF-8 Markdown result from the approved public audio fixture; the local route did not invoke the YouTube pipeline, and the source audio remained present and byte-identical.
- Loopback GUI smoke at `127.0.0.1:17862` returned HTTP 200, showed no public share URL, and stopped cleanly.
- Artifact inspection is clean; generated audio/transcript remain under ignored `temp/` paths.
- Follow-up Spec Kit converge found no remaining unbuilt work; no new tag or GitHub Release was created.
- Implementation commit `9f72a35806eb97114210d7d1159675e2bcb28997` is pushed to `origin/main`; GitHub Actions run `35529270503` completed with `success`.

## v1.1 next autonomous task

Complete the remaining handoff only: record the converged feature's commit/run evidence and stop for repository review. Do not publish a new release or begin unrelated features.
