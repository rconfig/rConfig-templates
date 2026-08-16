# xFTP: inbound file service

Most devices are backed up by rConfig connecting out to them, logging in and running commands.
Some cannot be. They will only push a file outward on their own schedule, or their configuration
is a binary archive that no CLI will print.

xFTP is the inbound side for those devices. rConfig runs a file service, the device pushes its
configuration in, and a sweeper picks the file up and files it against the right device.

**Ordinary configuration backups do not need xFTP.** If your device presents a CLI that rConfig
can log into, use a normal connection template. Reach for this only when the device genuinely
cannot be pulled from.

Behaviour described here was verified against rConfig Pro 8.3.2. Later releases may differ.

## Transports

Three transports can be enabled, each as a container managed by rConfig.

| Transport | Default port | Trust |
| --- | --- | --- |
| SFTP | operator chosen, mapped to 22 in the container | **Preferred.** Encrypted transport and authentication |
| FTP | 21, with a passive data range | Credentials and payload cross the network in clear text. Use only on a trusted management segment |
| TFTP | 69/udp | **No authentication at all.** Anything that can reach the port can write. Use only on an isolated management network, and never where the segment is shared |

Pick SFTP unless something about the device makes it impossible. TFTP is common on older network
hardware precisely because it is simple, and simple here means unauthenticated.

## How a pushed file finds its device

The sweeper runs on a schedule, looks at what has arrived, and works out which device each file
belongs to. It tries two things in order.

**1. Configured file matching rules.** Each rule belongs to a device and has a pattern and a type:

| Type | Matches |
| --- | --- |
| `exact` | The whole filename |
| `prefix` | The start of the filename |
| `suffix` | The end of the filename |
| `contains` | Anywhere in the filename |
| `regex` | A regular expression |

Rules are tried in order and the first match wins.

**2. Falling back to the device ID in the filename.** If no rule matches, the sweeper looks for a
numeric rConfig device ID in the filename, in this order:

```text
12345-anything.cfg          the ID at the very start, followed by a hyphen
device-12345-backup.cfg     an ID preceded by device, dev or id, joined by - or _
```

The ID must belong to a real device or the match is rejected. This fallback is why naming a pushed
file with its rConfig device ID is the simplest arrangement: it works with no rules configured at
all.

If neither approach identifies a device, the file is left where it is rather than being filed
against the wrong device.

### Date tokens in patterns

Patterns may contain date tokens, which is what makes a rule survive a filename that carries a
timestamp.

```text
{pattern.year}   {pattern.month}   {pattern.day}
{pattern.hour}   {pattern.minute}  {pattern.second}

{current.year}   {current.month}   {current.day}
{current.hour}   {current.minute}  {current.second}
```

The two families behave differently, and the difference matters:

- **`{pattern.*}`** matches **any** valid value for that unit. `{pattern.year}` matches any four
  digit year. Use this for a rule that should keep working tomorrow.
- **`{current.*}`** is replaced with **today's** value at match time. `{current.day}` only matches
  files carrying today's day number.

So a device pushing `core-sw-20260816.cfg` daily wants
`core-sw-{pattern.year}{pattern.month}{pattern.day}.cfg`, not the `current` form.

Braces must balance, and only the units listed above are accepted.

## What happens to a matched file

The file is moved into the device's own directory under rConfig's file store. If a file of that
name is already there, a timestamp is inserted before the extension rather than overwriting the
existing copy.

## The template in this directory

`xftp-inbound-only.yml` marks a device as inbound only. It tells rConfig not to connect out at
all: no SSH, no telnet, no script. Reachability is established by ping instead, since there is no
session to succeed or fail.

Assign it to the device, then arrange for the device to push its file.

Per the comments in the template itself, `xftp` is the protocol value on rConfig Pro releases
**newer than 8.3.2**. Releases up to and including 8.3.2 accept only `ftp` for inbound-only
devices. Check which your server is running before assuming a value.

## Device-side push commands

See [examples/push-commands.md](examples/push-commands.md) for starter commands across nine
platforms, and for the important limitation on which placeholder variables rConfig substitutes
into device commands.

## See also

- [docs/EDITIONS.md](../../docs/EDITIONS.md) for the Core and Pro split
- [docs/TEMPLATES.md](../../docs/TEMPLATES.md) for the template key reference
