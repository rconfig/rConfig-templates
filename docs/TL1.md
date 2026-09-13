# TL1

TL1 (Telcordia GR-831) is how optical transport gear is managed. It is not a CLI, and treating it
as one is where most of the surprises come from.

rConfig supports three TL1 platforms. Their templates live with their vendor, like every other
template in this library: `ciena/`, `infinera/`, `cisco/`.

| Vendor | Templates | Status |
| --- | --- | --- |
| Ciena 6500 | [`ciena/`](../ciena/) | `community-tested` |
| Infinera DTN-X | [`infinera/`](../infinera/) | `community-tested` |
| Cisco ONS 15454 | [`cisco/`](../cisco/) | `untested-starter`, see [cisco/README.md](../cisco/README.md) |

TL1 is a **Pro-only** protocol on every vendor. See [EDITIONS.md](EDITIONS.md).

## What is the same everywhere

**There is no enable mode, no pager to turn off, and no configuration save step**, so TL1
templates leave all three empty.

**Login is in-band.** The node opens on a bare prompt and waits for an `ACT-USER` command, which
rConfig sends itself. Whether the transport underneath authenticates first is the `sshAuth` key:
`password` for SSH auth then `ACT-USER`, `none` when `ACT-USER` is the only gate.

**Every command is terminated by `;`** and correlated by a CTAG that the node echoes back.

**Passwords are always sent quoted.** This started as a Ciena fix, and it is not Ciena-specific:
quoting keeps a password containing `:`, the TL1 field separator, from mis-framing the command on
any platform.

**Gateways front elements that have no management access of their own.** You connect to the
gateway; the elements behind it are addressed in-band by putting their TID in the command. Set
`tl1Gateway: "on"` on the **gateway's** template and rConfig discovers them after each collection
and creates a device record for each one.

An element can be **dual-homed**, reachable through two or more gateways. rConfig identifies an
element by its TID, so one reported by a second gateway gains a second path rather than a
duplicate device record. One gateway is primary; if a session through it cannot be established,
the collection falls over to another.

Typical retrieval commands to attach in an rConfig Command Group:

```text
RTRV-EQPT::ALL:100;
RTRV-ALM-ALL::ALL:101;
RTRV-SW-VER:::102;
```

## What differs by vendor, and why it matters

`tl1Vendor` selects the dialect. It defaults to `ciena`, so a template written before there was
more than one vendor keeps working untouched.

| | `ciena` | `infinera` | `cisco-ons` |
| --- | --- | --- | --- |
| Prompt | `<` | `>` | `<` |
| Elements called | RNEs | remote nodes | ENEs |
| Neighbour command | `RTRV-NE-LIST` | `RTRV-TIDMAP` | `RTRV-MAP-NETWORK` |
| Record format | keyword, quoted | keyword, empty AID | **positional** |
| Response | one block | **paged** | one block |

Three things follow from that table.

**The prompt differs.** Leave the device's Main Prompt blank in the UI and the dialect supplies
the right one. A `<` typed into an Infinera device's prompt field will hang the session until it
times out.

**Infinera pages its answer.** One logical response arrives as several blocks with the prompt
written between them. rConfig reads to the end of the response rather than to the first prompt.
Nothing to configure; it matters because a client that gets this wrong does not merely truncate
the list, it leaves the remaining blocks on the wire where they are read as the reply to the next
command.

**Cisco reports each element's own address and model.** The other two do not, so their elements
show the gateway's address as a placeholder.

## Connection limits

Every element collection opens its **own** session to the gateway. A gateway fronting a hundred
elements would otherwise see a hundred sessions attempted as fast as the queue can run them, and a
node that refuses connections past its own cap fails whichever collections lose that race.

`tl1MaxConnections` caps how many sessions rConfig opens to one gateway at a time. It defaults to
`20` and belongs on the **gateway's** template; elements inherit their gateway's limit rather than
carrying one of their own.

```yaml
connect:
  tl1Vendor: ciena
  tl1Gateway: "on"
  tl1MaxConnections: 20
```

A collection that finds no free slot is not a failure: nothing was dialled, so the device is not
marked unreachable and no failure notification is sent. It waits and retries, giving up after an
hour. A dual-homed element whose primary gateway is at capacity uses its other gateway instead of
waiting.

Set it to what the node itself will accept. Too high and the node refuses connections; too low and
a large gateway takes longer to work through its elements. Values outside 1 to 500 are clamped,
and anything non-numeric falls back to the default, so a typo cannot stop a gateway collecting.

## `tl1NeighbourCmd`

Optional, and best left out. Each vendor's own command is the default. Set it only to override the
verb, for example to pass an AID a particular node needs.

Templates predating multi-vendor support named `RTRV-NBR`, which no shipped node answers. rConfig
substitutes the vendor's real command and logs a warning rather than discovering nothing. Update
the template when you see that warning.

See [TEMPLATES.md](TEMPLATES.md) for what each key means and [CONTRIBUTING.md](CONTRIBUTING.md)
before submitting a change.
