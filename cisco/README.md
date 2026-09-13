# Cisco

The largest directory in the library, and now a mixed-edition one: the IOS, ASA, SMB and WLC
templates run on Core and Pro, and the two ONS 15454 TL1 templates are Pro only. That is the same
rule every other directory follows, which is that a template lives with its hardware. See
[docs/EDITIONS.md](../docs/EDITIONS.md).

| Template | Use for | Edition |
| --- | --- | --- |
| `cisco-ios-ssh-enable.yml` | IOS / IOS-XE over SSH, enable password required | Core, Pro |
| `cisco-ios-ssh-noenable.yml` | IOS / IOS-XE over SSH, account already at privilege 15 | Core, Pro |
| `cisco-ios-telnet-enable.yml` | IOS / IOS-XE over telnet, enable password required | Core, Pro |
| `cisco-ios-telnet-enable-nousername.yml` | IOS / IOS-XE over telnet, password-only login with no username prompt | Core, Pro |
| `cisco-ios-telnet-noenable.yml` | IOS / IOS-XE over telnet, account already at privilege 15 | Core, Pro |
| `cisco-asa-ssh-enable.yml` | ASA firewalls over SSH | Core, Pro |
| `cisco-smb-telnet-noenable.yml` | Small Business switches (SG/SF series) over telnet | Core, Pro |
| `cisco-wlc-ssh-noenable.yml` | Wireless LAN Controllers, SSH only, see below | Core, Pro |
| `cisco-ons15454-tl1-ssh.yml` | ONS 15454 optical nodes, TL1 on the SSH channel | **Pro** |
| `cisco-ons15454-tl1-telnet.yml` | ONS 15454 optical nodes, TL1 over raw TCP | **Pro** |

## ONS 15454 (TL1)

> **Status: `untested-starter`.** These two templates and the parser behind them were built from
> the Cisco ONS SONET TL1 Command Guide R9.1 and Oracle's ONS 15454 TL1 reference. **Nobody has run
> them against a real node.** Documented is better than invented and weaker than seen on hardware.
> If you run these, please report what happened so they can move to `community-tested`.

Read [docs/TL1.md](../docs/TL1.md) for what TL1 is and how gateways work. What is particular to an
ONS 15454:

**Cisco calls the elements behind a gateway ENEs** (End NEs). Ciena calls them RNEs, and rConfig's
UI uses Ciena's term.

**`RTRV-MAP-NETWORK` records are positional**, not keyword-based:

``text
"172.20.222.225,TID-000,15454"
 <IPADDR>       ,<NODENAME>,<PRODUCT>
``

`NODENAME` is the TID. `PRODUCT` is the only place any TL1 vendor reports a real platform per
element, so discovered ENEs carry their own model rather than the gateway's. The vendor
documentation notes `PRODUCT` comes back as `UNKNOWN` for a node running a different software
version; rConfig does not store that as a model.

**A gateway lists itself** in its own network map. rConfig drops that record, so the gateway is not
reconciled as an element behind itself.

### `tl1NeighbourCmd`

Optional. Leave it unset and `tl1Vendor: cisco-ons` supplies `RTRV-MAP-NETWORK`. Set it to send a
different verb, for example to pass an AID a particular node needs, and rConfig sends exactly
what you wrote.

**One value is not honoured.** A command beginning with `RTRV-NBR` is replaced with `RTRV-MAP-NETWORK`
and a warning is written to the activity log. rConfig shipped `RTRV-NBR:ALL` as the default
before 8.4.0, and that verb and its payload format came from rConfig's own simulator rather than
from hardware, so honouring it means discovering nothing at all. The substitution exists so an
estate upgrading from an older release keeps collecting while its templates are updated.

This is the one place rConfig overrides a value you set deliberately. If you have a node that
genuinely answers `RTRV-NBR`, say so on the issue tracker and the special case will be removed.

## FTD firewalls (1120 and similar)

Use the standard Cisco IOS SSH template, but set the device's prompt in the rConfig UI to `'>'`:
a single quote, a greater-than, and a single quote. Without it the backup is truncated.

## WLC controllers

Cisco WLC controllers implement SSH and telnet in a way that breaks most automation. Three rules:

- Use `cisco-wlc-ssh-noenable.yml`. No other template in this directory works.
- Use SSH. Telnet does not work reliably against these controllers.
- Do not run `show run-config`; it takes far too long to print. Use `show run-config commands`
  instead for the running configuration.

Background: [CSCve45024](https://quickview.cloudapps.cisco.com/quickview/bug/CSCve45024).

See [docs/TEMPLATES.md](../docs/TEMPLATES.md) for what each key means and
[docs/CONTRIBUTING.md](../docs/CONTRIBUTING.md) before submitting a change.
