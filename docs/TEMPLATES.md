# rConfig connection template legend

Complete reference for every key rConfig reads from a connection template.

A connection template describes **how rConfig talks to a device**: which protocol, which port,
which prompts to expect, how to get into enable mode, how to turn paging off, how to close the
session. That is all it describes.

A connection template does **not** hold the commands whose output you want to capture. Retrieval
commands attach to devices in rConfig through Command Groups, not through the template. If you
are looking for where `show running-config` lives, it is a Command Group, not this file.

---

## The on/off trap, read this first

rConfig parses templates with `symfony/yaml` v8.1.2, which follows YAML 1.2. That means:

```yaml
paging: on       # string "on"
paging: "on"     # string "on"     - identical to the line above
enable: yes      # string "yes"
enable: true     # BOOLEAN true    - NOT the string "true"
paging: off      # string "off"
paging: no       # string "no"
```

`on`, `off`, `yes` and `no` stay **strings** whether you quote them or not. Only `true`, `false`,
`null` and `~` become non-strings.

Nearly every switch in the connection code compares against the **string** `"on"` or `"yes"`, and
several of those comparisons are strict. So a YAML boolean does not match, and the behaviour you
asked for silently does not happen. There is no warning and no log line.

Worse, the failure is not even consistent between keys:

| You write | What happens |
| --- | --- |
| `paging: true` | Paging is **not** disabled. The comparison is strict, `true` is not `"on"`. |
| `enable: true` | Enable mode **is** entered. The comparison is loose, and a boolean comparison casts the other side to boolean. |

Two keys, the same mistake, opposite outcomes.

**The rule: always write `on` or `off` (or `yes` where a key expects it). Never write `true` or
`false` in a connection template.** Quoted or unquoted makes no difference, so pick one and stay
consistent.

Keys affected: `enable`, `paging`, `hpAnyKeyStatus`, `AnsiHost`, `isMikrotik`, `sshInteractive`,
`syncToPromptOnLogin`, `hasSplashScreen`, `hasSplashScreenEnterKey`, `enableUsername`.

---

## What "mandatory" means here

rConfig does not validate templates against a schema. It parses the YAML and then reads keys out
of the resulting array. How a key is read determines what happens when it is missing.

| Read style | Missing key behaviour | Shown in tables as |
| --- | --- | --- |
| Unguarded array access | Raises `Undefined array key`, value becomes `null`, connection continues with a null | **Mandatory** |
| Null-coalesced (`?? x`) | Falls back to the stated default | **Optional**, default shown |
| Guarded by `isset()` | Falls back to `null` | **Optional**, default `null` |

So "mandatory" does not mean rConfig refuses to run. It means the key is read without a guard: a
template that omits it produces a PHP warning and then behaves unpredictably rather than failing
cleanly. Always supply every mandatory key.

---

## Anatomy of a template

### The header block

Every template opens with the standard header applied by `scripts/apply_headers.py`. It carries
the edition the template targets, its verification status, which rConfig versions it has been
seen working on, the filename it replaced during the 2026 restructure, and the documentation
links. The header is comments only. rConfig never reads it.

### `main`

Identity. The template's unique name and the description shown in the rConfig UI. Neither value
influences the connection in any way, but `main.name` must be unique across the whole template
library because rConfig keys templates by it. Read on SSH, telnet and TL1; not read at all for
script templates.

### `connect`

Transport. Which protocol to speak, which port to dial, how long to wait. This is also where the
Pro-only extras live: the TL1 transport and gateway settings, the script idle timeout, and the
protocol fallback settings. `connect.protocol` is the one key that decides everything else,
because it selects which manager class runs and therefore which of the remaining sections are
read at all.

### `auth`

Getting logged in. Prompt strings for username and password, whether enable mode is needed and
how to reach it, the HP "press any key" quirk, and the flag that switches SSH to private key
authentication. Note that these are **prompt patterns**, not credentials. Real usernames,
passwords and keys come from the device record or a credential set, never from the template.
Read on SSH and telnet only.

### `vt100`

Splash screens. Some devices present a menu or banner that must be dismissed before a CLI prompt
appears. This section says whether that happens, what text to read up to, and which control code
to send to get past it. Read on SSH and telnet, with one key that is SSH only.

### `config`

Session behaviour. Paging on and off, the commands to disable and restore it, the command to save
configuration, the command to end the session, plus the MikroTik and prompt-sync workarounds.
This is the section with the most protocol asymmetry: several keys are read on both protocols but
acted on by only one.

### `options`

Terminal emulation for SSH. ANSI handling and terminal sizing, used mainly by HP and MikroTik
devices whose output is full of VT100 escape codes. Read on telnet too, but never acted on there.

### `failure_criteria`

Script templates only, Pro only. Decides whether a script run counts as a failure, by exit code,
by error patterns in the output, or by the absence of success patterns. Optional as a whole.

---

## `main`

| Key | Type | Values | Mandatory / Default | Protocols | Edition | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| `name` | string | free text | Mandatory | ssh, telnet, tl1 | Core and Pro | Must be unique across the library. Does not affect the connection. `SSH/Connect.php:85`, `Telnet/Connect.php:74`, `TL1/Connect.php:63`; Core `SSH/Connect.php:81`, `Telnet/Connect.php:71` |
| `desc` | string | free text | Mandatory | ssh, telnet, tl1 | Core and Pro | UI description only. `SSH/Connect.php:86`, `Telnet/Connect.php:75`, `TL1/Connect.php:64`; Core `SSH/Connect.php:82`, `Telnet/Connect.php:72` |

Script templates never build a connection object, so neither key is read for `protocol: script`.

---

## `connect`

| Key | Type | Values | Mandatory / Default | Protocols | Edition | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| `protocol` | string | `ssh`, `telnet`, `script`, `tl1`, `ftp` | Mandatory | dispatcher | Core: `ssh`, `telnet`. Pro: all five | **Case sensitive in the dispatcher**: `SSH` does not match `ssh`. The fallback and inbound-only paths lowercase first, so the same value is treated case-insensitively there and case-sensitively here. `ftp` has no dispatcher branch; it is handled earlier in the download path. `MainConnectionManager.php:50,56,62,68`; Core `:25,29`; `ConnectionParams.php:33`; `ProtocolFallbackConnectionManager.php:220-229` |
| `port` | int | 1 to 65535 | Mandatory | ssh, telnet, tl1 | Core and Pro | A device port override always wins over this value. The per-protocol classes apply no range check to the override; only the fallback manager does. `SSH/Connect.php:90`, `Telnet/Connect.php:79`, `TL1/Connect.php:69`, `ProtocolFallbackConnectionManager.php:75-90` |
| `timeout` | int | seconds | Mandatory on ssh, telnet, tl1. Default `30` on script | all | Core and Pro | Passed straight to the SSH2 constructor, and restored after prompt sync. Script uses it as a process timeout with its own default. `SSH/Connect.php:157`, `SSH/Login.php:91`, `Script/ScriptConnectionManager.php:33` |
| `isNonInteractiveMode` | string | truthy value | Optional, default none | ssh | Core and Pro | Switches command sending to a non-interactive exec instead of prompt-driven reads. Combines with `sshPrivKey` in the read-strategy order below. `SSH/Connect.php:91`, `SSH/SendCommand.php:24-50` |
| `idletimeout` | int | seconds | Optional, default `30` | script | **Pro only** | All lowercase. `Script/ScriptConnectionManager.php:34` |
| `sshAuth` | string | `none`, or anything else for password | Optional, default `password` | tl1 | **Pro only** | `none` skips transport authentication before the TL1 `ACT-USER` login. `TL1/Connect.php:70`, `Transport/SshTransport.php:33` |
| `tl1Transport` | string | `telnet`, or anything else for ssh | Optional, default `ssh` | tl1 | **Pro only** | Anything that is not literally `telnet` falls back to SSH. `TL1/Connect.php:71`, `Transport/Tl1TransportFactory.php:15-20` |
| `tl1Gateway` | boolean or string | `true`, `on`, `1`, `yes` | Optional, default `false` | tl1 | **Pro only** | The one key that accepts both a YAML boolean and the string forms, case-insensitively. Enables neighbour discovery. `TL1/Connect.php:93-95` |
| `tl1NeighbourCmd` | string | a TL1 command | Optional, default `RTRV-NBR:ALL` | tl1 | **Pro only** | Only used when `tl1Gateway` is on. `TL1/Connect.php:97` |
| `fallbackProtocol` | string | `ssh`, `telnet` | Optional, default none | dispatcher | **Pro only** | Undocumented before this legend. Set it to the other protocol and rConfig resolves which one the device actually answers on, caches the result, then dispatches normally. Only activates when it differs from `protocol` and both are ssh or telnet. `ProtocolFallbackConnectionManager.php:28,50-55,64` |
| `fallbackPort` | int | 1 to 65535 | Optional, defaults to 22 for ssh or 23 for telnet | dispatcher | **Pro only** | Undocumented before this legend. Port used for the fallback attempt. A device port override still wins. `ProtocolFallbackConnectionManager.php:30,70-91` |
| `probeTimeout` | int | clamped to 1 to 10 | Optional, falls back to `timeout`, then `5` | dispatcher | **Pro only** | Undocumented before this legend. Seconds to wait when testing whether a port is open. Values outside 1 to 10 are clamped. `ProtocolFallbackConnectionManager.php:190-196` |

---

## `auth`

Every value here is a **prompt pattern** or a switch. No credential ever lives in a template.

| Key | Type | Values | Mandatory / Default | Protocols | Edition | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| `username` | string | prompt pattern | Mandatory | ssh, telnet | Core and Pro | On telnet, an empty value skips the username step entirely. `SSH/Connect.php:94`, `Telnet/Connect.php:81`, `Telnet/Login.php:30-33` |
| `password` | string | prompt pattern | Mandatory | ssh, telnet | Core and Pro | `SSH/Connect.php:95`, `Telnet/Connect.php:82` |
| `enable` | string | `on`, `off` | Mandatory | ssh, telnet | Core and Pro | **Loose comparison.** `enable: true` also activates enable mode, unlike `paging`. Use `on` or `off`. `SSH/Login.php:46`, `Telnet/Login.php:37`; Core `SSH/Login.php:41`, `Telnet/Login.php:38` |
| `enableCmd` | string | CLI command | Mandatory | ssh, telnet | Core and Pro | Sent after reading the enable prompt. On SSH, any `~` in the value is escaped before use. `SSH/Login.php:253,281-287`, `Telnet/Login.php:68` |
| `enablePassPrmpt` | string | prompt pattern | Mandatory | ssh, telnet | Core and Pro | On SSH, any `~` is escaped before use. `SSH/Login.php:260,281-287`, `Telnet/Login.php:69` |
| `enableUsername` | string | `on` | Optional, default none | **ssh only** | Core and Pro | Strict comparison. Telnet has no equivalent branch, so a telnet device that asks for a username at enable time cannot be handled. `SSH/Login.php:255-258` |
| `enableUsernamePrmpt` | string | prompt pattern | Optional, default none | **ssh only** | Core and Pro | Only used when `enableUsername` is on. `SSH/Connect.php:99`, `SSH/Login.php:256` |
| `hpAnyKeyStatus` | string | `on` | Mandatory | ssh, telnet | Core and Pro | Strict comparison. On SSH it sends two newlines after login, and also selects a VT100 character-scrubbing read path. `SSH/Login.php:274`, `SSH/SendCommand.php:127`; Core `SSH/Login.php:193`, `SSH/SendCommand.php:88` |
| `hpAnyKeyPrmpt` | string | prompt string | Mandatory | **none, see dead keys** | Core and Pro | Read on both protocols and never used. `SSH/Connect.php:102`, `Telnet/Connect.php:87` |
| `sshInteractive` | string | `on` or `yes` | Optional, default none | **ssh only** | Core and Pro | The only key that accepts both spellings. Forces a manual read-and-write login instead of the library login. `SSH/Login.php:187`; Core `:109` |
| `sshPrivKey` | boolean or string | any truthy value | Optional, default none | **ssh only** | Core and Pro | A flag, not key material. When truthy, rConfig loads the actual private key and passphrase from the credential set attached to the device. Telnet reads this key and ignores it. `SSH/Login.php:142-146,162-173`, `Telnet/Connect.php:89` |

---

## `vt100`

For devices that show a menu or banner before the CLI prompt.

| Key | Type | Values | Mandatory / Default | Protocols | Edition | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| `hasSplashScreen` | string | `on` | Optional, default none | ssh, telnet | Core and Pro | **SSH compares strictly, telnet compares loosely.** `SSH/Login.php:192`, `Telnet/Login.php:23` |
| `hasSplashScreenEnterKey` | string | `on` | Optional, default none | **ssh only** | Core and Pro | Sends a newline before reading the splash text. Telnet never reads it, so a telnet splash screen cannot be given an initial Enter. `SSH/Login.php:196-199` |
| `splashScreenReadToText` | string | text to read up to | Optional, default none | ssh, telnet | Core and Pro | `SSH/Login.php:201`, `Telnet/Login.php:26` |
| `splashScreenSendControlCode` | string | control code to send | Optional, default none | ssh, telnet | Core and Pro | `SSH/Login.php:202`, `Telnet/Login.php:27` |

---

## `config`

| Key | Type | Values | Mandatory / Default | Protocols | Edition | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| `paging` | string | `on` | Mandatory | ssh (telnet reads, does not act) | Core and Pro | Strict comparison, so `paging: true` silently does nothing. **On SSH this gates whether `pagingCmd` is sent. On telnet it does not: telnet sends `pagingCmd` unconditionally.** `SSH/Login.php:241,264`, `SSHConnectionManager.php:108,118`, `Telnet/Login.php:44-45` |
| `pagingCmd` | string | CLI command | Mandatory | ssh, telnet | Core and Pro | On SSH, sent only when `paging` is on, and any `~` is escaped first. On telnet, always sent after login regardless of `paging`. `SSH/Login.php:239-247,281-287`, `Telnet/Login.php:44-45` |
| `resetPagingCmd` | string | CLI command | Mandatory | ssh, telnet | Core and Pro | **Different gates per protocol.** SSH sends it at disconnect only when `paging` is on. Telnet sends it whenever the value is non-empty, with no `paging` check. `SSHConnectionManager.php:106-112`, `SSH/SendCommand.php:164-168`, `Telnet/Quit.php:38-43` |
| `saveConfig` | string | CLI command | Mandatory | **telnet only** (ssh reads, does not act) | Core and Pro | Sent on telnet teardown when non-empty. Read into an SSH property and never sent. `Telnet/Quit.php:45-51`, `SSH/Connect.php:117` |
| `exitCmd` | string | CLI command | Mandatory | **telnet only** (ssh reads, does not act) | Core and Pro | Sent on telnet teardown when non-empty, and by the fallback probe (which deliberately skips `saveConfig`, because a probe must never write config). Read into an SSH property and never sent. `Telnet/Quit.php:53-58`, `PrimaryProtocolVerifier.php:83-95`, `SSH/Connect.php:118` |
| `isMikrotik` | string | `yes` | Optional, default none | **ssh only** | Core and Pro | Strict comparison. Sends one Enter past the MikroTik banner at login, then blanks the device prompt for reads so output is captured with a match-anything pattern. `SSH/Login.php:97,95-128`, `SSH/SendCommand.php:43,45,67,68` |
| `linebreak` | string | `n`, `r` | Mandatory | **none, see dead keys** | Core and Pro | Read on both protocols and never used. `SSH/Connect.php:109`, `Telnet/Connect.php:91` |
| `syncToPromptOnLogin` | string | `on` | Optional, default `off` | **ssh only** | **Pro only** | Undocumented before this legend. Set it when command output appears under the wrong command: it drains any prompt the login sequence left unread, so the first command waits for its own prompt. `SSH/Connect.php:113`, `SSH/Login.php:63-93` |
| `promptSyncTimeout` | int | seconds | Optional, default `2` | **ssh only** | **Pro only** | Undocumented before this legend. How long to wait for another prompt during the sync above before deciding the device is quiet. Capped at 10 reads. `SSH/Connect.php:114`, `SSH/Login.php:79` |
| `pagerPrompt` | string | any | Optional, default none | **none, see dead keys** | Core and Pro | Deprecated. Read and never used. Must not appear in new templates. `SSH/Connect.php:115`, `Telnet/Connect.php:95` |
| `pagerPromptCmd` | string | any | Optional, default none | **none, see dead keys** | Core and Pro | Deprecated. Read and never used. Must not appear in new templates. `SSH/Connect.php:116`, `Telnet/Connect.php:96` |

---

## `options`

Terminal emulation. Functional on SSH. Read on telnet and never acted on: the telnet source
carries an explicit comment saying these are kept only for consistency.

| Key | Type | Values | Mandatory / Default | Protocols | Edition | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| `AnsiHost` | string | `yes` | Optional, default none | **ssh only** | Core and Pro | Strict comparison. Selects the ANSI read path, which strips VT100 escape codes from output. Needed by HP and MikroTik devices. `SSH/SendCommand.php:39`; Core `:37` |
| `setWindowSize` | array | `[columns, rows]` | Optional, default none | **ssh only** | Core and Pro | Applied to the SSH session as a real window size. `SSH/Connect.php:136,158-160` |
| `setTerminalDimensions` | array | `[width, height]` | Optional, default none | **ssh only** | Core and Pro | Affects ANSI post-processing only, not the negotiated terminal. Used to size the ANSI screen when the ANSI read path runs. For very large configurations, raise the second value. `SSH/Connect.php:138,161-163`, `SSH/SendCommand.php:61-63` |

---

## `failure_criteria`

Script templates only. Pro only. The whole section is optional.

| Key | Type | Values | Mandatory / Default | Protocols | Edition | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| `exit_codes` | array of int | e.g. `[1, 2, 255]` | Optional, omitted | **script only** | **Pro only** | When listed, this is an allowlist: only these codes count as failure. An empty list `[]` opts out of exit-code checking entirely. Omitting the key means any non-zero exit code fails, the Unix convention. `Script/ScriptConnectionManager.php:64-73` |
| `error_patterns` | array of string | substrings | Optional, omitted | **script only** | **Pro only** | Matched against stdout and stderr combined. Any match fails the run. `Script/ScriptConnectionManager.php` |
| `success_patterns` | array of string | substrings | Optional, omitted | **script only** | **Pro only** | Any match means success. `Script/ScriptConnectionManager.php` |

---

## What each protocol actually reads

| Protocol | Sections read | Edition |
| --- | --- | --- |
| `ssh` | `main`, `connect`, `auth`, `vt100`, `config`, `options` | Core and Pro |
| `telnet` | `main`, `connect`, `auth`, `vt100`, `config`, `options` (last two partly ignored) | Core and Pro |
| `tl1` | `main` and `connect` only. No `auth`, `config`, `options` or `vt100` key is read | Pro only |
| `script` | `connect` and `failure_criteria` only. No connection object is built | Pro only |
| `ftp` | `connect.protocol` only. Handled in the download path, never dispatched | Pro only |

### SSH read-strategy order

When sending each command, SSH picks a read strategy. First match wins:

1. `sshPrivKey` and `isNonInteractiveMode` both set, use exec
2. `sshPrivKey` set, use the ANSI path
3. `isNonInteractiveMode` set, use exec
4. `AnsiHost` is `yes`, use the ANSI path
5. `isMikrotik` is `yes`, blank the prompt then use the standard path
6. Otherwise, the standard path

Evidence: `SSH/SendCommand.php:24-50`.

### Prompt matching differs by protocol

SSH matches prompts as regular expressions delimited by `~`, and pre-escapes any `~` found in
`pagingCmd`, `enableCmd`, `enablePassPrmpt` and the device prompt before use
(`SSH/Login.php:281-287`).

Telnet builds its pattern as `/<prompt>$/` with **no escaping and no delimiter protection**, and
anchors the match to the end of the buffer (`Telnet/Read.php:49`). A device prompt containing `/`
therefore works on SSH and breaks on telnet.

### Strict and loose comparisons

Strict, so a YAML boolean will not match: `paging`, `hpAnyKeyStatus`, `AnsiHost`, `isMikrotik`,
`sshInteractive`, `syncToPromptOnLogin`, `enableUsername`, and `hasSplashScreen` on SSH.

Loose: `enable` on both protocols, `hasSplashScreen` on telnet, `hasSplashScreenEnterKey`.

---

## Dead keys

These keys exist but do nothing. They are documented here so nobody spends an afternoon tuning a
value that is never read. **They are still present in shipped templates. Removing them is a
separate change, not covered by this document.**

### Read by rConfig, never acted upon

| Key | Section | Why it does nothing |
| --- | --- | --- |
| `linebreak` | `config` | Assigned to a property on both protocols and never referenced again in either edition. `SSH/Connect.php:109`, `Telnet/Connect.php:91` |
| `hpAnyKeyPrmpt` | `auth` | Assigned on both protocols and never referenced. The only remaining consumer is commented out. `SSH/Connect.php:102`, `Telnet/Connect.php:87` |
| `pagerPrompt` | `config` | Deprecated. Its consumer in the telnet read loop is commented out. `SSH/Connect.php:115`, `Telnet/Read.php:25,80-86` |
| `pagerPromptCmd` | `config` | Deprecated. No consumer anywhere in either codebase. `SSH/Connect.php:116`, `Telnet/Connect.php:96` |
| `saveConfig` on SSH | `config` | Read into an SSH property and never sent. Works normally on telnet. `SSH/Connect.php:117` |
| `exitCmd` on SSH | `config` | Read into an SSH property and never sent. Works normally on telnet. `SSH/Connect.php:118` |

### Present in templates, read by no code

| Key | Section | Files carrying it | Why it does nothing |
| --- | --- | --- | --- |
| `ctrlYLogin` | `connect` | `avaya/avaya-ers-ssh-noenable-vector.yml` | The name does not occur anywhere in either codebase. That device's control-code login is actually driven by its `vt100` section |
| `idleTimeout` | `connect` | `SIE-Base/script_template.yml`, `SIE-Radware/alteon_expect_script_template.yml` | rConfig reads `idletimeout`, all lowercase. Key lookup is case sensitive, so this never matches and the 30 second default always applies |
| `linebreak` inside `auth` | `auth` | `hp/hp-1920-ssh-enable.yml` | rConfig only ever reads `config.linebreak`. Misplaced into the wrong section, and `config.linebreak` is itself unused |

Three distinct keys across four files.

For contrast, `vt100` is **not** dead. Four shipped templates use it and both editions read it:
`avaya/avaya-ers-ssh-noenable-vector.yml`, `avaya/avaya-ers-telnet-noenable.yml`,
`fortinet/fortinet-fortios-ssh-noenable-banner.yml`,
`siemens/siemens-ruggedcom-ros-ssh-noenable.yml`.

---

## Requesting a new key

Adding a key to the template format means adding code that reads it. That is an rConfig product
change, not a template change, so it starts before any pull request here.

1. **Work out the order of operations first.** Describe the exact point in the session where the
   new behaviour has to happen: after authentication but before paging, between enable mode and
   the first command, at teardown, and so on. The connection code is a fixed sequence, and a new
   key has to slot into it somewhere specific. If you cannot name that point, the request is not
   ready.
2. **Show why the existing keys cannot express it.** Work through this legend and say which keys
   you tried and how each fell short. Many device quirks are already covered by a key that is not
   obviously named for the symptom, so check `syncToPromptOnLogin`, `isMikrotik`, `AnsiHost`,
   `sshInteractive` and the `vt100` section before concluding nothing fits.
3. **Attach a sanitized session transcript.** Capture the real device session showing the
   behaviour, with hostnames, IP addresses, usernames, passwords, community strings and serial
   numbers removed. The transcript is what makes the request actionable: it shows exactly what
   the device sends and when.

A dedicated issue form is being prepared. Until it lands, open a normal issue on this repository
including the three items above.

---

## Validation

`scripts/validate_templates.py` will check templates against this legend: mandatory keys present,
values within the documented sets, no dead keys, no YAML booleans where a string is required.

That script arrives in a later phase. This line is a forward reference. Until it exists, check
new templates against the tables above by hand.

---

## Verification record

This legend was compiled from a full read of the rConfig connection stack in both editions.

| | |
| --- | --- |
| Compiled | 2026-08-16 |
| rConfig Pro analysed | V8.3.2, commit `832e530` |
| rConfig Core analysed | branch `develop`, commit `cdcb518`, app version 8.2.15 |
| YAML parser | `symfony/yaml` v8.1.2 |
| Evidence file | `legend-evidence.md` |

Coverage: 46 keys across 7 top-level sections. Core reads 33 of them. The 13 that are Pro only
are the four TL1 keys, the three fallback keys, `idletimeout`, `sshAuth`, `syncToPromptOnLogin`,
`promptSyncTimeout`, and the three `failure_criteria` keys.

Line references point at the two codebases above. They are accurate as of those commits and will
drift as the code changes. Re-verify against the evidence file before relying on a specific line.
