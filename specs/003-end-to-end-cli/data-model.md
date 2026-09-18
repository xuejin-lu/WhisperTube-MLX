# Data Model: End-to-End CLI Pipeline

- **PipelineRequest**: URL, temporary audio directory, transcript output directory, model, and downloader/browser options.
- **PipelineRun**: request, optional acquired audio path, optional transcript path, and terminal stage.
- **TemporaryAudioArtifact**: current-run regular file below the temporary root; cleanup eligible.
- **TranscriptArtifact**: returned Markdown path; never cleanup eligible.
