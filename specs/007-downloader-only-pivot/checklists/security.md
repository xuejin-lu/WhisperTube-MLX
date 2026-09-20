# Security Checklist: Downloader-Only Pivot

**Purpose**: Review the downloader requirements for privacy, scope, and safe local
file/credential boundaries before implementation.
**Created**: 2026-09-21
**Feature**: [Downloader-Only Pivot](../spec.md)

**Review Ownership**: This is a reviewer-owned requirements-quality artifact.
`[x]` means the requirement itself has been reviewed and is sufficiently complete;
it does not mean implementation is complete.

## Local data and credentials

- [x] CHK001 Does the spec clearly state that media remains on the local Mac and is never uploaded automatically? [Completeness, Spec §1/§10]
- [x] CHK002 Does the spec define the exact default output root and prevent accidental writes to repository runtime directories? [Clarity, Spec §7]
- [x] CHK003 Does the cookie fallback requirement say that browser cookies are opt-in, local-only, never exported, and never committed? [Completeness, Spec §10]
- [x] CHK004 Does the launcher requirement explicitly prohibit browser launches and credential capture? [Completeness, Spec §8/§10]
- [x] CHK005 Are setup reruns and cleanup boundaries specified so user downloads, cookies, and caches are not deleted? [Edge case, Spec §8/§9]

## Command and URL safety

- [x] CHK006 Does the spec distinguish explicit playlist URLs from watch URLs containing `list=`? [Clarity, Spec §5]
- [x] CHK007 Are supported video URL forms and invalid/non-YouTube behavior sufficiently bounded for deterministic validation? [Coverage, Spec §5/§13]
- [x] CHK008 Does the format requirement explicitly exclude MP3 re-encoding and arbitrary post-processing? [Clarity, Spec §6]
- [x] CHK009 Does the output naming requirement define deterministic templates without allowing user input to become an unintended command argument? [Security, Spec §5/§7]
- [x] CHK010 Is the requirement to use argv/argument-safe command construction explicit enough to prevent shell injection? [Gap/Clarity, Spec §8/§13]

## Failure and scope boundaries

- [x] CHK011 Does playlist failure behavior define continuation, visible skipped/failed reporting, and a final summary without silently hiding errors? [Completeness, Spec §11]
- [x] CHK012 Are missing dependency, invalid URL, download failure, and output failure user-visible with actionable recovery? [Coverage, Spec §8/§13]
- [x] CHK013 Does the spec explicitly prohibit transcription, MLX, OpenCC, Gradio, localhost servers, and Colab automation from the normal workflow? [Scope, Spec §4/§12]
- [x] CHK014 Does the spec define that historical v1.0.0 artifacts remain immutable while current mainline complexity is reduced? [Consistency, Spec §4/§12]
- [x] CHK015 Are real smoke-test boundaries explicit so public test media is temporary and never committed? [Privacy, Spec §14]

## Notes

- Review these items as requirements-quality checks before implementation.
- Resolve gaps in `spec.md`, `plan.md`, or `tasks.md` before checking an item.
