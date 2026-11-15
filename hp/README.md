# HP and HPE

Covers HP ProCurve and HP Comware switches, including H3C branded Comware hardware. All templates
run on Core and Pro. Aruba AOS-S switches, the later name for the ProCurve line, are in
[aruba/](../aruba/).

## ProCurve

ProCurve switches show a "Press any key to continue" screen after login and decorate their output
with VT100 terminal codes, which trips up most automation. The SSH templates set
`hpAnyKeyStatus: on`, which sends the keystrokes to get past that screen and cleans the terminal
codes from the captured output.

| Template | Use for |
| --- | --- |
| `hp-procurve-ssh-noenable.yml` | The standard choice. Start here |
| `hp-procurve-ssh-noenable-nopage.yml` | Firmware without the swallowed-character quirk below |
| `hp-procurve-telnet-noenable.yml` | ProCurve over telnet |

`hp-procurve-ssh-noenable.yml` sends `"nno page"` as its paging command. The doubled letter is
DELIBERATE. Some HPE firmware swallows the first character sent after the any-key prompt, so the
extra letter is sacrificial and the switch receives `no page` as intended. Do not correct it.

`hp-procurve-ssh-noenable-nopage.yml` sends the plain `no page` command instead. Switch to it if
you see an `Invalid input: nno` style error in the session logs.

The telnet template sets `saveConfig: "wr mem"`. Telnet sessions send `saveConfig` when they close,
so every telnet backup saves the configuration on the switch. Clear the value in your copy if you
do not want that. SSH sessions never send it.

## Comware

| Template | Use for |
| --- | --- |
| `hp-comware-ssh-noenable.yml` | Comware switches, including H3C branded hardware |
| `hp-comware-ssh-noenable-flexfabric.yml` | FlexFabric switches |
| `hp-comware-ssh-noenable-nosystemview.yml` | The A5120, without entering system-view |
| `hp-comware-5400xl-ssh-noenable.yml` | The 5400xl |
| `hp-1920-ssh-enable.yml` | The 1920, which needs a special elevation command other HP switches do not |

All Comware templates turn paging off with `screen-length disable`.

**The 1920** uses the enable step to send `_cmdline-mode on` and the `y` that confirms it, both
inside `enableCmd`.

**The 5400xl** template carries `enableUsername: on` with `Please Enter Login Name:` and
`Please Enter Password:` prompts, for switches that ask for a username and password when entering
privileged mode. The template ships with `enable: off`, so those keys do nothing until you set
`enable: on` in your copy. Enable usernames are handled over SSH only.

**The A5120** template sets `enableCmd: "system-view"`, but with `enable: off` that command is never
sent. The template connects and collects without entering system-view, as its name says.

See [docs/TEMPLATES.md](../docs/TEMPLATES.md) for what each key means and
[docs/CONTRIBUTING.md](../docs/CONTRIBUTING.md) before submitting a change.
