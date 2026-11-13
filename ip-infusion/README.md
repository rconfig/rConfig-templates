# IP Infusion

Covers IP Infusion OcNOS over SSH, on OcNOS-SP and OcNOS-DC. Pick the template by whether the
device lets you into enable mode.

| Template | Use for |
| --- | --- |
| `ip-infusion-ocnos-ssh-enable.yml` | Licensed devices. Logs in at user mode (`host>`), then runs `enable` |
| `ip-infusion-ocnos-ssh-noenable.yml` | Devices without an installed license, which refuse `enable` |

To check, log in by hand and type `enable`. If the prompt changes from `host>` to `host#`, use the
enable template. If OcNOS refuses the command, use the no enable template.

## Enable password

OcNOS does not ask for a password at `enable`. Leave the enable password on the credential set
blank. The enable template matches the privileged prompt (`host#`) instead of a password prompt.

## Device prompts

Set the prompts on each device record from its hostname:

| Template | Main prompt | Enable prompt |
| --- | --- | --- |
| `ip-infusion-ocnos-ssh-enable.yml` | `^R1-CE1#` | `^R1-CE1>` |
| `ip-infusion-ocnos-ssh-noenable.yml` | `^AS7326-56X-1>` | `^AS7326-56X-1>` |

## Snippets

OcNOS uses a transaction-based CLI. Changes made in `configure terminal` only take effect after
`commit`, so end every config snippet with `commit` and then `end`. Both templates leave
`saveConfig` empty, so a backup never writes to the device.

Both templates carry `snippet_errors`, so rConfig Pro V8.4.1 and later send snippets one line at a
time and stop at the first rejected line. `% Un-committed transactions present` catches a snippet
that reaches `end` without `commit`.

When the device prompt starts with `^`, add a `config_prompt` directive as the first line of the
snippet, so rConfig recognises the exec prompt and every `(config...)#` prompt:

```text
#[config_prompt /(?:^|\n)(?:\w|\.|-)+(?:\((?:\w|-)+\))?#\s*$/]
```

## Typical retrieval commands

```text
show running-config
show version
show interface brief
show system-information board-info
```

Both templates were verified by the rConfig team against OcNOS-SP 7.0.0 to 7.1.0 and OcNOS-DC
6.6.1 to 7.0.1, on UfiSpace and Edgecore hardware.

See [docs/TEMPLATES.md](../docs/TEMPLATES.md) for what each key means and
[docs/CONTRIBUTING.md](../docs/CONTRIBUTING.md) before submitting a change.
