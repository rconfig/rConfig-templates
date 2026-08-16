# Pre and post change snapshot

Captures a device's operational state as a delimited text snapshot, for running either side of a
change window.

| File | What it is |
| --- | --- |
| `pre-post-change-snapshot-script.yml` | The SIE template |
| `pre-post-change-snapshot.sh` | The script, bash over SSH |

## How to use it

Run it once before the change and once after. rConfig stores each run as a version, so **the diff
between the two is the evidence of what the change actually did.** Not what the change request
said it would do, and not what anyone remembers doing at two in the morning.

This is worth having even when the change goes perfectly, because it is the artefact that proves
it did.

## What it captures

```text
show running-config
show ip interface brief
show ip route summary
show cdp neighbors detail
show version
```

Each section is wrapped in a `===== command =====` delimiter. That is not decoration: without a
fixed delimiter, a single line moving between sections shows up in the diff as two unrelated
changes, and a genuinely small change gets lost in the noise.

Adapt the command list for your platform. The delimiters matter more than the specific commands.

## Environment

| Variable | Required | Purpose |
| --- | --- | --- |
| `SNAPSHOT_HOST` | yes | Device hostname or IP |
| `SNAPSHOT_USER` | yes | SSH username |
| `SNAPSHOT_PORT` | no | Defaults to 22 |

Authentication is by SSH key. `BatchMode=yes` is set, so the script fails cleanly rather than
hanging on a password prompt.

## Output streams

The configuration goes to stdout and becomes the stored backup. Progress lines and the
success marker go to stderr, so the stored artefact is exactly the configuration and nothing
else. `error_patterns` and `success_patterns` are matched against stdout and stderr combined,
so putting the marker on stderr does not stop it being detected.

## Failure criteria

The template omits `exit_codes` deliberately. Omitted means any non-zero exit fails the run.
Listing an allowlist would record a crash with an unlisted code as a success, which is the
opposite of what you want from a backup job.
