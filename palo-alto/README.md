# Palo Alto Networks

Covers PAN-OS firewalls over SSH. All three templates run on Core and Pro and expect a `login as:`
username prompt.

| Template | Use for |
| --- | --- |
| `palo-alto-panos-ssh-enable.yml` | PAN-OS over SSH. Uses the enable step to turn scripting mode on. Start here |
| `palo-alto-panos-9x-ssh-noenable.yml` | PAN-OS 9.x, with no enable step. Turns the pager off with `set cli pager off` |
| `palo-alto-panos-ssh-enable-vector.yml` | PAN-OS reached from a Vector agent |

PAN-OS has no enable mode in the Cisco sense. Two of the templates use rConfig's enable step simply
to send PAN-OS CLI settings straight after login, since `enableCmd` is sent as written:

- `palo-alto-panos-ssh-enable.yml` sends `set cli scripting-mode on`.
- `palo-alto-panos-ssh-enable-vector.yml` sends `set cli pager off` and
  `set cli config-output-format set`, then uses its paging command to enter `configure`.

## Terminal settings and large configurations

The standard and 9.x templates carry an `options` block:

```yaml
options:
  AnsiHost: "yes"
  setWindowSize: [240, 2048]
  setTerminalDimensions: [260, 1000]
```

`AnsiHost: "yes"` selects the ANSI read path, which strips terminal escape codes such as `^[[K`
from the output. `setTerminalDimensions` sizes the screen that path uses, as columns and rows. For
firewalls with very large configurations, raise the second value towards the number of lines in
the configuration; values up to 50000 have been needed. A larger capture can also need a higher
PHP `memory_limit` on the rConfig server (the default is 256M).

If a template returns partial configs, try removing the whole `options` block from your copy as a
first test.

## Saving

`saveConfig` is set to `commit` in the standard and 9.x templates, but SSH sessions never send
`saveConfig`, so a backup does not commit anything. See [docs/TEMPLATES.md](../docs/TEMPLATES.md).

See [docs/TEMPLATES.md](../docs/TEMPLATES.md) for what each key means and
[docs/CONTRIBUTING.md](../docs/CONTRIBUTING.md) before submitting a change.
