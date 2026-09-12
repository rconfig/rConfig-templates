# Ciena

Covers Ciena 6500 optical nodes, managed over TL1 rather than a conventional CLI.

| Template | Use for |
| --- | --- |
| `ciena-6500-tl1-ssh.yml` | 6500 nodes reached over SSH, TL1 carried on the SSH channel |
| `ciena-6500-tl1-telnet.yml` | 6500 nodes reached over raw TCP on a TL1 port, typically 3082/3083 |

Typical retrieval commands to attach in an rConfig Command Group:

```text
RTRV-EQPT::ALL:100;
RTRV-ALM-ALL::ALL:101;
RTRV-SW-VER:::102;
```

## TL1 is not a CLI

There is no enable mode, no pager to turn off, and no configuration save step, so these templates
leave all three empty. Login is in-band: the node opens on a bare `<` prompt and waits for an
`ACT-USER` command, which rConfig sends itself. Every command is terminated by `;` and correlated
by a CTAG that the node echoes back.

Passwords are always sent quoted. A 6500 rejects a complex password sent bare, and quoting also
keeps a password containing `:` — the TL1 field separator — from mis-framing the command.

## Gateway and remote NEs

Optical networks are reached through a **Gateway NE (GNE)**, the node you actually connect to,
which fronts **Remote NEs (RNEs)** that have no management access of their own. Set
`tl1Gateway: "on"` on the GNE's template and rConfig runs `tl1NeighbourCmd` after collecting it,
discovers the RNEs behind it, and creates a device record for each one. RNEs are then collected
by addressing their TID in-band over a session to the GNE.

An RNE can be **dual-homed** — reachable through two or more GNEs. rConfig identifies an RNE by
its TID, so an RNE reported by a second gateway gains a second path rather than a duplicate device
record. One gateway is the primary; if a session through it cannot be established, the collection
falls over to another.

## Connection limits

Every RNE collection opens its **own** session to the gateway. A GNE fronting a hundred RNEs would
otherwise see a hundred sessions attempted as fast as the queue can run them, and a node that
refuses connections past its own cap fails whichever collections lose that race.

`tl1MaxConnections` caps how many sessions rConfig opens to one gateway at a time. It defaults to
`20` and belongs on the **GNE's** template — RNEs inherit their gateway's limit rather than
carrying one of their own.

```yaml
connect:
  tl1Gateway: "on"
  tl1MaxConnections: 20
```

A collection that finds no free slot is not a failure: nothing was dialled, so the device is not
marked unreachable and no failure notification is sent. It waits and retries, giving up after an
hour. A dual-homed RNE whose primary gateway is at capacity will use its other gateway instead of
waiting.

Set it to what the node itself will accept. Too high and the node refuses connections; too low and
a large gateway takes longer to work through its RNEs. Values outside 1 to 500 are clamped, and
anything non-numeric falls back to the default, so a typo cannot stop a gateway collecting.

See [docs/TEMPLATES.md](../docs/TEMPLATES.md) for what each key means and
[docs/CONTRIBUTING.md](../docs/CONTRIBUTING.md) before submitting a change.
