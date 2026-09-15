# Data Model: Local YouTube Audio Acquisition

## Video Request

Represents one user-provided request for a single YouTube video.

| Field | Type | Rules |
|---|---|---|
| original_url | text | Required input; must use `http` or `https`. |
| normalized_url | text | Canonical `https://www.youtube.com/watch?v=...` URL. |
| video_id | text | Required; exactly 11 characters from `[A-Za-z0-9_-]`. |
| playlist_parameters | query values | Ignored for v0.1 selection; never cause batch processing. |

### State transitions

`received → validated → acquiring → completed` or `received → rejected`; an acquisition failure
transitions to `failed` and must not be reported as completed.

## Local Audio Artifact

Represents the temporary output produced for one completed Video Request.

| Field | Type | Rules |
|---|---|---|
| path | local path | Must be beneath the configured ignored runtime directory. |
| video_id | text | Matches the associated Video Request. |
| container_extension | text | Preserved from the selected source format in v0.1. |
| lifecycle | enum | Temporary runtime data; not committed or uploaded. |

## Browser Session Source

Represents an optional local browser session used only when anonymous acquisition is blocked.

| Field | Type | Rules |
|---|---|---|
| browser | text | A browser identifier accepted by the local downloader. |
| credential_location | local protected storage | Read by the downloader; never copied to repository files. |
| use | enum | Explicit retry only; absent from the anonymous request. |

## Relationships

- One Video Request may produce zero or one Local Audio Artifact per invocation.
- One Video Request may optionally reference one Browser Session Source during a retry.
- Browser Session Source is never persisted as application data.
