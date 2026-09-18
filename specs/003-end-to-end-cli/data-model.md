# Data Model: End-to-End CLI Pipeline

- **PipelineRequest**: URL, temporary audio directory, transcript output directory, model, and downloader/browser options.
- **PipelineRun**: request, dedicated current-run acquisition directory, optional acquired audio path,
  optional transcript path, and terminal stage.
- **TemporaryAudioArtifact**: current-run regular file below the temporary root; cleanup eligible. A
  partial artifact is cleanup eligible only when it remains inside the default acquirer's dedicated
  current-run directory.
- **PipelineFailure**: original stage category/exit code plus optional cleanup-failure context and
  residual-artifact risk.
- **TranscriptArtifact**: returned Markdown path; never cleanup eligible.
