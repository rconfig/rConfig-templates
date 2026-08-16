# Script Integration Engine: base template

`script_template.yml` is the starter to copy when writing a Script Integration Engine template.
Copy it into a vendor subdirectory here, rename it to the convention, and adjust the failure
criteria for your script.

SIE runs an external script instead of opening a CLI session. Use it when a device has no usable
CLI, or when getting the configuration out needs logic that a prompt-driven connection template
cannot express.

## What a script template carries

A `protocol: script` template is much smaller than a connection template, because rConfig never
opens a socket for it.

| Key | Purpose |
| --- | --- |
| `connect.protocol` | Must be `script` |
| `connect.timeout` | Seconds the process may run in total. Defaults to 30 when absent |
| `connect.idletimeout` | Seconds the process may sit idle. Defaults to 30 when absent |
| `failure_criteria` | Decides whether the run failed. Optional as a whole |

Both templates here carry **two spellings of the idle timeout**. `idletimeout`, all lowercase, is
the spelling the current code reads. `idleTimeout` in camelCase is kept alongside it for forward
compatibility. Key lookup is case sensitive, so the lowercase one is the one that takes effect
today. Keep both, and keep them the same value.

## Failure criteria

All three keys are optional and each behaves differently when omitted.

**`exit_codes`** is an allowlist of codes that mean failure.

- Listed, for example `[1, 2, 255]`: only those codes fail the run
- Empty list `[]`: a deliberate opt-out, exit status alone never fails the run
- Omitted entirely: the Unix convention applies, any non-zero exit code fails the run

**`error_patterns`** is a list of substrings matched against the script's standard output and
standard error combined. Any match fails the run.

**`success_patterns`** is a list of substrings where any single match means success.

## What does not apply

No socket is opened and no connection object is built for a script template, so none of the
session keys are read: nothing from `auth`, nothing from `config`, nothing from `options`,
nothing from `vt100`. `main.name` and `main.desc` are not read either, although `main.name` must
still be unique across the library because rConfig keys templates by it in the UI.

Do not copy an SSH template as a starting point for a script template. Everything below `connect`
would be dead weight.

## Attaching the script

Scripts attach to a device through rConfig Command Groups, the same way retrieval commands do for
a CLI device. The template says how to run, the Command Group says what to run.

See [docs/TEMPLATES.md](../../../docs/TEMPLATES.md) for the full key reference and
[docs/EDITIONS.md](../../../docs/EDITIONS.md) for the Core and Pro split. Vendor documentation for
the feature is at
<https://docs.rconfig.com/integrations/script-integration-engine/sie/>.
