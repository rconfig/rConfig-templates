# SSH non-interactive mode

`connect.isNonInteractiveMode` changes how an SSH template sends show commands. Instead of writing
each command to the interactive shell and reading until the device prompt returns, rConfig sends it
over an SSH exec channel and takes whatever comes back as the output. No prompt matching is involved
for those commands.

It suits devices whose interactive shell is hard to read reliably: prompts that are unstable, output
that wraps or redraws, or sessions that pause unpredictably. FortiGate and MikroTik templates in
this repository use it:

- [fortinet/fortinet-fortios-ssh-noenable-noninteractive.yml](../fortinet/fortinet-fortios-ssh-noenable-noninteractive.yml)
- [mikrotik/mikrotik-routeros-ssh-noenable-noninteractive-vector.yml](../mikrotik/mikrotik-routeros-ssh-noenable-noninteractive-vector.yml)

## Setting it

```yaml
connect:
  protocol: ssh
  isNonInteractiveMode: true
```

Core and Pro both read the key, on SSH only.

- **Pro** treats any truthy value as on. That includes the string `off`, which is a non-empty string.
  To turn the mode off, leave the key out of the template.
- **Core 8.2.16 and later** normalise the value to `on` or `off` first, so `true`, `on` and `yes`
  turn it on and `false`, `off` and `no` turn it off. Earlier Core releases use a truthy check, like
  Pro.

`true` works on every edition and version, which is why the templates use it.

## What it changes, and what it does not

- **Login is unchanged.** Authentication, banners, enable mode and the paging command all run as
  normal before the first command. See [ORDER-OF-OPERATIONS.md](ORDER-OF-OPERATIONS.md).
- **Show commands use the exec channel.** Each command is sent with a trailing `\r`, whatever
  `config.commandLinebreak` says.
- **Snippet sends are unaffected.** Snippets are still written to the interactive shell and read to
  the prompt.
- **It takes priority over the ANSI and MikroTik read paths.** When rConfig picks how to read each
  command, the order is: `sshPrivKey` with `isNonInteractiveMode` (exec), then `sshPrivKey` alone
  (ANSI), then `isNonInteractiveMode` alone (exec), then `AnsiHost`, then `isMikrotik`, then the
  standard path. See [TEMPLATES.md](TEMPLATES.md#ssh-read-strategy-order).

## Things to check

- Some devices refuse exec requests, or run them in a different context from the interactive shell.
  If every command comes back empty, try the same template without the key.
- Because the output is not read to a prompt, a device prompt that never matches does not show up
  as a timeout on show commands. It can still affect the login steps that read to the prompt.

See [TEMPLATES.md](TEMPLATES.md) for the full key reference.
