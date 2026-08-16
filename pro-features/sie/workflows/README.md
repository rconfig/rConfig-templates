# SIE workflow examples

Four worked examples of what the Script Integration Engine can do beyond running a single command.
Each directory holds a `protocol: script` template and the script it runs.

| Example | Language | Demonstrates |
| --- | --- | --- |
| [api-backup-meraki/](api-backup-meraki/) | python3, standard library | Backing up a device that has no CLI at all, over a REST API |
| [pre-post-change-snapshot/](pre-post-change-snapshot/) | bash | Capturing operational state either side of a change window, so the rConfig diff is the evidence |
| [multi-step-firewall-export/](multi-step-firewall-export/) | expect | A device that needs trigger, poll and fetch rather than one command |
| [database-config-dump/](database-config-dump/) | bash | Versioning something that is not a network device at all |

All four are `untested-starter`. They are patterns to adapt, not drop-in solutions: the prompts,
endpoints and command names are illustrative and will need changing for your environment.

## Conventions shared by all four

**Configuration on stdout, everything else on stderr.** Whatever the script prints to stdout is
the artefact rConfig stores. Progress and the success marker go to stderr so the stored backup
stays clean. `error_patterns` and `success_patterns` are matched against both streams, so a marker
on stderr is still detected.

**A definite success marker.** Each script emits its own `SIE-OK:` line, and the template's
`success_patterns` matches that exact string. An empty or truncated run does not produce it.

**`ERROR:` on failure, then a non-zero exit.** Each template lists `ERROR:` in `error_patterns`,
so a failure is caught by pattern as well as by exit code.

**`exit_codes` omitted.** Omitted means any non-zero exit fails the run. An allowlist would let a
crash with an unlisted code be recorded as a success.

**Configuration through environment variables.** The scripts read hostnames and credentials from
the environment rather than hard-coding them. Set them for the account that runs rConfig jobs.

## Attaching one of these

The template is assigned to the device the same way a connection template is. The script attaches
to the device through a Command Group, the same way a retrieval command does. See
[../_base/README.md](../_base/README.md) for what a script template carries.
