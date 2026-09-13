# Infinera

Covers Infinera DTN-X optical nodes, managed over TL1 rather than a conventional CLI.

| Template | Use for |
| --- | --- |
| `infinera-dtnx-tl1-ssh.yml` | DTN-X nodes reached over SSH, TL1 carried on the SSH channel |
| `infinera-dtnx-tl1-telnet.yml` | DTN-X nodes reached over raw TCP on a TL1 port, typically 3082/3083 |

**Read [docs/TL1.md](../docs/TL1.md) first.** It covers what TL1 is, in-band `ACT-USER` login,
gateways and dual-homed elements, and `tl1MaxConnections`. What follows is only what is particular
to a DTN-X, and two of these three items will bite anyone assuming Ciena's behaviour.

## The prompt is `>`

Not `<`. **Leave the device's Main Prompt blank in the rConfig UI** and the dialect supplies the
right one. A `<` typed in there will hang the session until it times out.

## The response is paged

`RTRV-TIDMAP` returns one logical answer as several blocks: every block but the last is coded
`RTRV` rather than `COMPLD`, with the prompt written between them.

rConfig reads to the end of the response rather than to the first prompt, so there is nothing to
configure. It is worth knowing because the failure mode is not a truncated list. A client that
stops at the first prompt leaves the remaining blocks in the socket, where they are read back as
the reply to the *next* command, and every command after that is answered out of step.

## The response header carries the system name, not the TID

A DTN-X relaying a command for another node still answers under its own system name:

``text
   LXTNKYXAO4Z 26-09-12 19:53:38
M  3 COMPLD
``

even when the command addressed `STLTND1Y`. So a routed reply cannot be confirmed by comparing the
header to the TID, the way it can on a 6500. rConfig knows this and does not apply that check to
this platform. Do not "fix" it.

## `tl1NeighbourCmd`

Optional. Leave it unset and `tl1Vendor: infinera` supplies `RTRV-TIDMAP`. Set it to send a
different verb, for example to pass an AID a particular node needs, and rConfig sends exactly
what you wrote.

**One value is not honoured.** A command beginning with `RTRV-NBR` is replaced with `RTRV-TIDMAP`
and a warning is written to the activity log. rConfig shipped `RTRV-NBR:ALL` as the default
before 8.4.0, and that verb and its payload format came from rConfig's own simulator rather than
from hardware, so honouring it means discovering nothing at all. The substitution exists so an
estate upgrading from an older release keeps collecting while its templates are updated.

This is the one place rConfig overrides a value you set deliberately. If you have a node that
genuinely answers `RTRV-NBR`, say so on the issue tracker and the special case will be removed.

---

## Records

``text
"::TID=CSVLTNFCO1Y,NODEID=MA4623110007,ROUTERID=11.253.152.33"
``

Keyword fields with an empty AID. `ROUTERID` is a routing identifier despite being shaped like an
address, so rConfig does not store it as the node's management IP: discovered nodes show their
gateway's address instead.

See [docs/TEMPLATES.md](../docs/TEMPLATES.md) for what each key means and
[docs/CONTRIBUTING.md](../docs/CONTRIBUTING.md) before submitting a change.
