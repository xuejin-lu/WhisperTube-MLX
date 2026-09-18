# Research: End-to-End CLI Pipeline

## Decision 1: Reuse callable boundaries

Use adapters around existing modules; pipeline owns sequencing and cleanup only. Shelling out or
copying stage internals would lose deterministic error behavior or duplicate approved logic.

## Decision 2: Cleanup only current-run audio

Keep the returned acquisition path and unlink it in a `finally` path only if it resolves below the
configured temporary root. Missing files are already clean; other cleanup errors are reported.

## Decision 3: Preserve error causes

Wrap acquisition exceptions as a download category, re-raise transcription errors unchanged, and use
a cleanup category only when cleanup follows successful transcription.
