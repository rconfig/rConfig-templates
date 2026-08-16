# Core and Pro

Which template capabilities work on which edition of rConfig.

## Read this as a support matrix

This document states what is **supported**, which is not always the same question as what the
code contains. Where the two differ, both are stated on the row, and the support position is what
governs. A capability whose code exists in Core but which is not supported there is still not
something to build on in Core.

The simple version, which covers most people:

- **Templates in vendor directories run on Core and Pro.** If it is in `cisco/`, `arista/`,
  `hp/` or any other vendor directory, both editions can use it.
- **Everything under `pro-features/` requires Pro.** That is the Script Integration Engine
  templates and scripts, the SSH private key template, and the xFTP inbound-only template.

One exception to the directory rule is called out below: the two TL1 templates live in `ciena/`
because they are Ciena device templates, but TL1 itself is Pro only.

## Capability matrix

| Capability | Core | Pro | Notes |
| --- | --- | --- | --- |
| `protocol: ssh` | Yes | Yes | The bulk of the library |
| `protocol: telnet` | Yes | Yes | |
| `protocol: script` (Script Integration Engine) | No | Yes | Templates and example scripts live in `pro-features/sie/` |
| `protocol: tl1` | No | Yes | The two templates live in `ciena/` because they are Ciena device templates, but the protocol is Pro only |
| Inbound-only devices (`xftp` / `ftp`) | No | Yes | The device pushes its configuration in rather than rConfig connecting out. `xftp` is the canonical value on releases after 8.3.2; `ftp` is the value on 8.3.2 and earlier. See `pro-features/xftp/` |
| Protocol fallback (`fallbackProtocol`, `fallbackPort`, `probeTimeout`) | No | Yes | Resolves which protocol a device actually answers on, then caches it. No shipped template uses these keys yet |
| Prompt sync on login (`syncToPromptOnLogin`, `promptSyncTimeout`) | No | Yes | The fix for output appearing under the wrong command |
| `auth.sshPrivKey` | **Not supported** | Yes | Code to read this key is present in Core, but private key authentication is supported on Pro only. This is a support position, not a code gate: it may appear to work in Core and is still not supported there. The template lives in `pro-features/ssh-private-key/` |

## The 13 Pro-only keys

Of the 46 keys in [TEMPLATES.md](TEMPLATES.md), 13 are read only by Pro.

| Section | Keys |
| --- | --- |
| `connect`, TL1 | `sshAuth`, `tl1Transport`, `tl1Gateway`, `tl1NeighbourCmd` |
| `connect`, fallback | `fallbackProtocol`, `fallbackPort`, `probeTimeout` |
| `connect`, script | `idletimeout` |
| `config`, prompt sync | `syncToPromptOnLogin`, `promptSyncTimeout` |
| `failure_criteria` | `exit_codes`, `error_patterns`, `success_patterns` |

**The other 33 keys are Core-capable.** Every key in `main`, `auth`, `vt100` and `options`, and
every key in `config` apart from the two prompt-sync keys, is read by both editions.

Note that `auth.sshPrivKey` is counted among the 33 because Core contains the code that reads it.
Per the row above, it is nonetheless not supported on Core.

## What Core gives you in practice

Core covers prompt-driven CLI devices over SSH and telnet, which is the large majority of network
hardware. Log in, optionally enter enable mode, turn paging off, run show commands, read the
output back to a prompt, close the session. Banner and splash-screen handling, the HP any-key
quirk, MikroTik banner sync, ANSI terminal handling and the enable-username variant are all
Core capabilities. If your devices present a normal CLI and you can reach them over SSH or telnet,
Core does the job.

## What Pro adds

**Script Integration Engine.** Runs an external script instead of opening a CLI session, for
devices with no usable CLI or where retrieval needs logic a template cannot express. Brings the
`failure_criteria` section, which decides whether a run failed by exit code, by error patterns in
the output, or by the absence of success patterns.

**TL1.** A different protocol entirely, used by optical transport equipment. Carries its own
transport selection, an optional gateway mode that discovers neighbouring nodes, and command
correlation by tag rather than by prompt matching.

**Inbound-only devices.** For hardware that pushes its configuration to rConfig rather than being
connected to. rConfig never dials out; reachability comes from ping instead.

**Protocol fallback.** Declare a second protocol and rConfig works out which one the device
actually answers on, caches the answer, and dispatches normally from then on. Useful across a
mixed estate where you do not know per device whether SSH is enabled.

**Prompt sync on login.** Drains any prompt the login sequence left unread, so the first command
waits for its own prompt. This is the fix when every command's output appears under the previous
command.

**SSH private key authentication.** Supported on Pro, as noted above.

## When this matrix is wrong

Support positions change, and this document is a snapshot maintained by hand. If something here
does not match what you observe, that is worth knowing about: please
[open an issue](https://github.com/rconfig/rConfig-templates/issues) saying which row, what you
saw, and on which rConfig version and edition. Do not assume the matrix is right and your device
is wrong.

For what each key does, see [TEMPLATES.md](TEMPLATES.md). For when each key fires during a
session, see [ORDER-OF-OPERATIONS.md](ORDER-OF-OPERATIONS.md).
