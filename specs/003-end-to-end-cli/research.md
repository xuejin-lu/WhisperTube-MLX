# Research: End-to-End CLI Pipeline

## Decision 1: Reuse callable boundaries

Use adapters around existing modules; pipeline owns sequencing and cleanup only. Shelling out or
copying stage internals would lose deterministic error behavior or duplicate approved logic.

## Decision 2: Cleanup only current-run audio

Keep the returned acquisition path and unlink it in a `finally` path only if it resolves below the
configured temporary root. The default acquirer also owns the dedicated `run-*` directory it creates
and removes that directory recursively if acquisition fails after producing partial artifacts.
Missing files are already clean; other cleanup errors are reported. Cleanup never extends to an
injected, pre-existing, or arbitrary path.

## Decision 3: Preserve error causes

Wrap acquisition exceptions as a download category and re-raise transcription errors with their
original class, category, and exit code. If cleanup also fails, append an actionable residual-audio
warning to that original failure. Use a cleanup category only when cleanup follows successful
transcription.
