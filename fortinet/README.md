# Fortinet

Covers FortiGate firewalls running FortiOS, over SSH. All four templates run on Core and Pro.

| Template | Use for |
| --- | --- |
| `fortinet-fortios-ssh-noenable.yml` | FortiGates without VDOMs. Start here |
| `fortinet-fortios-ssh-noenable-vdom.yml` | FortiGates with VDOMs enabled. The paging command enters `config global` first |
| `fortinet-fortios-ssh-noenable-banner.yml` | Devices with a pre-login banner that must be accepted by pressing `a` |
| `fortinet-fortios-ssh-noenable-noninteractive.yml` | Devices where prompt-driven reads are unreliable. Sends each command over a non-interactive exec channel |

FortiOS has no enable mode, so every template connects with `enable: off`.

## Paging

FortiOS turns paging off through the console settings rather than a one-line command, so
`pagingCmd` is a multi-line value: `config system console`, `set output standard`, `end`. The VDOM
template wraps it in `config global` and a second `end`, because console settings are global on a
VDOM device.

## Device prompts

Set the device's main prompt in the rConfig UI as `hostname #`, the format FortiOS uses. Do not put
a regex wildcard (`.*`) between the hostname and the `#`: a broad pattern can match a `#` inside
the configuration output and end the capture early. If the prompt contains `$`, escape it with a
backslash (`prompt\$`).

## The banner template

`fortinet-fortios-ssh-noenable-banner.yml` carries a `vt100` section. rConfig reads up to
`(Press 'a' to accept):` and sends `a`, then carries on with the login. Without it, a device with
that banner appears to hang, because rConfig waits for a prompt while the device waits for the
keypress.

## The non-interactive template

`fortinet-fortios-ssh-noenable-noninteractive.yml` sets `isNonInteractiveMode`, which sends each
command over an SSH exec channel and returns its output, instead of reading the interactive shell
to the prompt. See [docs/noninteractive-ssh.md](../docs/noninteractive-ssh.md) for how it works and
how it combines with other settings.

## Timeouts

The templates use a 5 second timeout. Long configurations (30,000 lines or more) need a higher
value.

See [docs/TEMPLATES.md](../docs/TEMPLATES.md) for what each key means and
[docs/CONTRIBUTING.md](../docs/CONTRIBUTING.md) before submitting a change.
