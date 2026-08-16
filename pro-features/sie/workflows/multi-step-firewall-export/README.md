# Multi step firewall export

For devices that cannot simply be asked for their configuration in one command.

| File | What it is |
| --- | --- |
| `multi-step-firewall-export-script.yml` | The SIE template |
| `multi-step-firewall-export.exp` | The script, expect |

## The pattern

1. **Log in.**
2. **Trigger** the export.
3. **Poll** until the device reports completion, with a bounded number of attempts.
4. **Fetch** the file and print its contents.
5. **Emit** the success marker.

Step 3 is the reason this example exists. A connection template can send a command and read to a
prompt; it cannot wait for an asynchronous job and then decide what to do next. That needs a
script.

## Adapt the prompts per platform

**The command names and prompt patterns in the script are illustrative.**
`request system export configuration`, `show system export status` and
`show file exported-configuration` are placeholders for whatever your platform actually uses.
The structure is the part worth copying, not the strings.

## Bounded polling

The loop gives up after 20 polls at 15 second intervals, and fails immediately if the device
reports a failure. Never write this loop unbounded: a device that never reports completion would
otherwise hold the job open until the template timeout kills it, with no useful error.

Note that `connect.timeout` in the template is the outer limit on the whole run, so it must be
larger than the worst case polling time you allow here.

## Environment

| Variable | Required | Purpose |
| --- | --- | --- |
| `FW_HOST` | yes | Device hostname or IP |
| `FW_USER` | yes | Username |
| `FW_PASSWORD` | yes | Password |
| `FW_PROMPT` | no | CLI prompt to expect, defaults to `#` |

## Output streams

The script keeps `log_user` off for the login and polling phases and turns it on only while the
exported file is being printed. The configuration goes to stdout and becomes the stored backup. Progress lines and the
success marker go to stderr, so the stored artefact is exactly the configuration and nothing
else. `error_patterns` and `success_patterns` are matched against stdout and stderr combined,
so putting the marker on stderr does not stop it being detected.

## Failure criteria

The template omits `exit_codes` deliberately. Omitted means any non-zero exit fails the run.
Listing an allowlist would record a crash with an unlisted code as a success, which is the
opposite of what you want from a backup job.
