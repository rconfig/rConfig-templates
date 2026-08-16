# Zyxel GS1900

| File | What it is |
| --- | --- |
| `zyxel-gs1900-ssh.exp` | An expect script that logs into a GS1900 over SSH and retrieves its configuration |

## Why this is a script and not a template

The GS1900 range presents a restricted CLI. It does not give you a normal shell that a
prompt-driven connection template can read to a prompt, so there is nothing for the usual
`pagingCmd` and prompt-matching machinery to work with. A connection template cannot drive it.

An expect script can, because it can handle the menu and prompt sequence directly rather than
relying on rConfig to match a prompt pattern.

This is the general test: if a device does not present a stable prompt that rConfig can read to,
it needs the Script Integration Engine rather than a connection template.

## Zyxel devices that do have a full CLI

The XGS range, the GS2xxx range and above present a Cisco-like CLI and work with an ordinary
connection template. Those live in [zyxel/](../../../zyxel/) at the repository root and run on
Core as well as Pro.

## Using this script

Pair it with a `protocol: script` template. Copy [../_base/script_template.yml](../_base/script_template.yml),
rename it to the convention, and set the failure criteria to match what this script returns.
Attach the script to the device through a Command Group.
