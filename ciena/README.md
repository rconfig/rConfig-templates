# Ciena

Covers Ciena 6500 optical nodes, managed over TL1 rather than a conventional CLI.

| Template | Use for |
| --- | --- |
| `ciena-6500-tl1-ssh.yml` | 6500 nodes reached over SSH, TL1 carried on the SSH channel |
| `ciena-6500-tl1-telnet.yml` | 6500 nodes reached over raw TCP on a TL1 port, typically 3082/3083 |

**Read [docs/TL1.md](../docs/TL1.md) first.** It covers what TL1 is, in-band `ACT-USER` login,
gateways and dual-homed elements, and `tl1MaxConnections`, none of which is Ciena-specific. What
follows is only what is particular to a 6500.

## The password quoting quirk

A 6500 rejects a complex password sent bare, which is what prompted rConfig to quote TL1 passwords
in the first place. rConfig now quotes on every vendor, so this is history rather than
configuration, but it is the reason the behaviour exists.

## Neighbour discovery

A 6500 answers `RTRV-NE-LIST` with one quoted record per remote NE:

``text
"SHELF-1::SID=\"RNE-LIMERICK\",NENAME=\"RNE-LIMERICK\",GNE=NO,GNEIPADDR=,INETADDR=10.0.254.3,COST=30,NETYPE=00011600"
``

`RTRV-NODES` reports the same set under different field names (`TID=`, `REMOTESHELF`, `IPADDR`,
`MEMBER`, `SITEID`) and rConfig parses either, so a template may use whichever a given release
answers.

`INETADDR` is the RNE's own management address, so discovered RNEs show their own IP rather than
the gateway's. `GNE=YES` marks a neighbour that is itself a gateway.

A 6500 echoes the addressed TID in the response header, so rConfig can confirm a routed reply came
from the RNE rather than from the gateway answering as itself. Not every vendor does this.

## `tl1NeighbourCmd`

Optional. Leave it unset and `tl1Vendor: ciena` supplies `RTRV-NE-LIST`. Set it to send a
different verb, for example to pass an AID a particular node needs, and rConfig sends exactly
what you wrote.

**One value is not honoured.** A command beginning with `RTRV-NBR` is replaced with `RTRV-NE-LIST`
and a warning is written to the activity log. rConfig shipped `RTRV-NBR:ALL` as the default
before 8.4.0, and that verb and its payload format came from rConfig's own simulator rather than
from hardware, so honouring it means discovering nothing at all. The substitution exists so an
estate upgrading from an older release keeps collecting while its templates are updated.

This is the one place rConfig overrides a value you set deliberately. If you have a node that
genuinely answers `RTRV-NBR`, say so on the issue tracker and the special case will be removed.

---

## Terminology

Ciena calls the elements behind a gateway **RNEs** (Remote NEs). Cisco calls them ENEs and
Infinera calls them remote nodes. They are the same idea, and rConfig's UI uses Ciena's term.

See [docs/TEMPLATES.md](../docs/TEMPLATES.md) for what each key means and
[docs/CONTRIBUTING.md](../docs/CONTRIBUTING.md) before submitting a change.
