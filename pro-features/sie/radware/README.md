# Radware Alteon

A worked example of a Script Integration Engine pair: a script template and the expect script it
runs.

| File | What it is |
| --- | --- |
| `radware-alteon-script-template.yml` | The SIE connection template. Sets the timeouts and the failure criteria |
| `alteon-cdump-test-script.exp` | An expect script that logs into an Alteon over SSH and drives a configuration dump |

## How the pair is used

The template is assigned to the device in rConfig, exactly like a connection template. The script
is attached to the device through a Command Group, exactly like a retrieval command. The template
governs how long the script may run and what counts as failure; the script does the work.

## What the example demonstrates

The expect script takes the device IP, username and password as its first three arguments, opens
an SSH session with relaxed key exchange and host key options for older Alteon firmware, handles
the login prompt and a confirmation prompt, then issues the dump.

The template's `failure_criteria` shows all three mechanisms in use at once:

- `exit_codes: [1, 2, 255]`, matching the exit codes the script itself returns on timeout and
  connection failure
- `error_patterns` for `Connection refused`, `Authentication failed` and `ERROR:`
- `success_patterns` for markers that appear in a good run, including a fallback on the Alteon
  main prompt

That last point is the useful part of the example: the success patterns are chosen from strings
the device actually emits, not from what the script hopes to see.

See [../_base/README.md](../_base/README.md) for what a script template carries and how the
failure criteria behave.
