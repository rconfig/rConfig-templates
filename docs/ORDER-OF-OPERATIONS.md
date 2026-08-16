# Order of operations

## A template is a script, not a bag of settings

The most common mistake in template authoring is treating a template as a list of options that
rConfig consults whenever it feels like it. It does not work that way.

rConfig runs a fixed sequence for each protocol: open the socket, authenticate, deal with the
banner, enter enable mode, turn paging off, send each command, tear the session down. **Every key
in a template acts at exactly one point in that sequence.** A key that would be perfect at step 6
does nothing at all if the behaviour you need happens at step 3.

This is why two templates with the same keys can behave completely differently, and why adding a
key that "looks right" often changes nothing. Once you know where in the sequence a key fires,
most template problems answer themselves.

For what each key means and what values it accepts, see [TEMPLATES.md](TEMPLATES.md). This
document is about **when** each key fires.

---

## SSH

Entry point `SSHConnectionManager::SSHConnectionAndOutput()`, `SSH/SSHConnectionManager.php:22-45`.

| Step | What happens | Keys driving it | Evidence |
| --- | --- | --- | --- |
| 1 | Build the parameters object from the template and device record | all sections | `SSH/Connect.php:81-152` |
| 2 | Port sanity check | `connect.port` | `SSH/Connect.php:156,170-177` |
| 3 | Open the SSH socket | `connect.port`, `connect.timeout` | `SSH/Connect.php:157` |
| 4 | Apply the terminal window size | `options.setWindowSize` | `SSH/Connect.php:158-160` |
| 5 | Stash the ANSI terminal dimensions for later | `options.setTerminalDimensions` | `SSH/Connect.php:161-163` |
| 6 | Escape `~` in every value that will be used as a regex | `config.pagingCmd`, `auth.enableCmd`, `auth.enablePassPrmpt`, device prompt | `SSH/Login.php:281-287` |
| 7 | Authenticate | `auth.sshPrivKey` decides key versus password | `SSH/Login.php:140-183` |
| 8 | HP "press any key" nudge, password path only | `auth.hpAnyKeyStatus` | `SSH/Login.php:154,272-279` |
| 9 | Manual interactive login, if requested | `auth.sshInteractive` | `SSH/Login.php:37-39,130-138` |
| 10 | Dismiss the splash screen | `vt100.hasSplashScreen`, `vt100.hasSplashScreenEnterKey`, `vt100.splashScreenReadToText`, `vt100.splashScreenSendControlCode` | `SSH/Login.php:41,190-203` |
| 11 | MikroTik banner sync, one Enter past "press Enter to continue" | `config.isMikrotik` | `SSH/Login.php:44,95-128` |
| 12a | If enable is on: enter enable mode, then send the paging command if paging is on | `auth.enableCmd`, `auth.enableUsername`, `auth.enableUsernamePrmpt`, `auth.enablePassPrmpt`, then `config.pagingCmd` | `SSH/Login.php:46-47,249-270` |
| 12b | Otherwise: send the paging command only | `config.paging`, `config.pagingCmd` | `SSH/Login.php:49,239-247` |
| 13 | Drain any prompt the login left unread | `config.syncToPromptOnLogin`, `config.promptSyncTimeout` | `SSH/Login.php:52,63-93` |
| 14 | For each command, choose a read strategy | `auth.sshPrivKey`, `connect.isNonInteractiveMode`, `options.AnsiHost`, `config.isMikrotik` | `SSH/SendCommand.php:24-50` |
| 15 | Read the output and clean it | `auth.hpAnyKeyStatus` or `auth.sshPrivKey` select the VT100 scrubbing path | `SSH/SendCommand.php:127-153` |
| 16 | Restore paging at teardown | `config.paging`, `config.resetPagingCmd` | `SSHConnectionManager.php:106-112` |
| 17 | Disconnect | none | `SSHConnectionManager.php:111` |

**Step 14 precedence, first match wins:**

1. `sshPrivKey` and `isNonInteractiveMode` both set, use exec
2. `sshPrivKey` set, use the ANSI path
3. `isNonInteractiveMode` set, use exec
4. `AnsiHost` is `yes`, use the ANSI path
5. `isMikrotik` is `yes`, blank the prompt then use the standard path
6. Otherwise, the standard path

**SSH never sends `config.saveConfig` or `config.exitCmd`.** Both are read into properties at
step 1 and discarded.

---

## Telnet

Entry point `TelnetConnectionManager::telnetConnectionAndOutput()`.

| Step | What happens | Keys driving it | Evidence |
| --- | --- | --- | --- |
| 1 | Build the parameters object | all sections | `Telnet/Connect.php:71 onward` |
| 2 | Open the socket | `connect.port`, `connect.timeout` | `Telnet/Connect.php` connect() |
| 3 | Dismiss the splash screen | `vt100.hasSplashScreen`, `vt100.splashScreenReadToText`, `vt100.splashScreenSendControlCode` | `Telnet/Login.php:23-28` |
| 4 | Send the username, only if the prompt value is not empty | `auth.username` | `Telnet/Login.php:30-33` |
| 5 | Send the password | `auth.password` | `Telnet/Login.php:35-36` |
| 6a | If enable is on: enter enable mode | `auth.enableCmd`, `auth.enablePassPrmpt` | `Telnet/Login.php:37-38,64-73` |
| 6b | Otherwise: read to the device prompt | none | `Telnet/Login.php:40` |
| 7 | **Send the paging command, always** | `config.pagingCmd` | `Telnet/Login.php:44-45` |
| 8 | Send each command and read to the prompt | device prompt | `Telnet/SendCommand.php:23-36` |
| 9 | Restore paging, if the value is not empty | `config.resetPagingCmd` | `Telnet/Quit.php:38-43` |
| 10 | Save configuration, if the value is not empty | `config.saveConfig` | `Telnet/Quit.php:45-51` |
| 11 | Send the exit command, if the value is not empty | `config.exitCmd` | `Telnet/Quit.php:53-58` |
| 12 | Close the socket | none | `Telnet/Quit.php:25` |

Two things catch people out here.

**Step 7 ignores `config.paging`.** On SSH the paging command is gated; on telnet it is sent
unconditionally after login. Setting `paging: off` on a telnet template does not stop the command
going out.

**Steps 9 to 11 are the only place `saveConfig` and `exitCmd` ever fire.** If your device needs a
clean logout, telnet is the only protocol that will give it one.

Telnet never reads `auth.enableUsername`, `auth.sshInteractive`, `connect.isNonInteractiveMode`,
`config.isMikrotik`, `config.syncToPromptOnLogin`, or `vt100.hasSplashScreenEnterKey`.

---

## TL1

Pro only. Entry point `Tl1ConnectionManager::tl1ConnectionAndOutput()`.

| Step | What happens | Keys driving it | Evidence |
| --- | --- | --- | --- |
| 1 | Build the parameters object | `main` and `connect` only | `TL1/Connect.php:60-98` |
| 2 | Normalise the prompt, defaulting a blank or lone `<` | device prompt | `TL1/Connect.php:84-87` |
| 3 | Select the byte transport | `connect.tl1Transport` | `TL1/Connect.php:101`, `Transport/Tl1TransportFactory.php:15-20` |
| 4 | Open the transport | `connect.port`, `connect.timeout` | `Transport/SshTransport.php`, `Transport/TelnetTransport.php` |
| 5 | Transport level authentication, skippable | `connect.sshAuth` set to `none` skips it | `Transport/SshTransport.php:33` |
| 6 | TL1 `ACT-USER` login, tagged with a CTAG | device credentials | `TL1/Login.php:68-84` |
| 7 | Send commands, correlating each response by CTAG | none | `TL1/SendCommand.php` |
| 8 | Neighbour discovery, if this node is a gateway | `connect.tl1Gateway`, `connect.tl1NeighbourCmd` | `TL1/Connect.php:93-97`, `TL1/Tl1NeighbourDiscovery.php` |

TL1 reads **no** key from `auth`, `config`, `options` or `vt100`. Paging, enable mode, save and
exit are all meaningless in a TL1 template. If you copy a working SSH template as a starting
point for TL1, everything below `connect` is dead weight.

---

## Script

Pro only. Entry point `ScriptConnectionManager::ScriptConnectionAndOutput()`,
`Script/ScriptConnectionManager.php:25-56`.

| Step | What happens | Keys driving it | Evidence |
| --- | --- | --- | --- |
| 1 | For each command, resolve and sanitise it | none | `Script/ScriptConnectionManager.php:29-31` |
| 2 | Run the process | `connect.timeout`, `connect.idletimeout` | `Script/ScriptConnectionManager.php:33-35` |
| 3 | Decide whether the run failed | `failure_criteria.exit_codes`, `failure_criteria.error_patterns`, `failure_criteria.success_patterns` | `Script/ScriptConnectionManager.php:57 onward` |

**No socket is opened and no connection object is built**, so `main`, `auth`, `config`, `options`
and `vt100` are never read for a script template.

---

## The FTP short circuit

Pro only. An inbound-only device never gets connected to at all.

There is no dispatcher branch for this protocol. The download path short-circuits first
(`DeviceConfigDownload.php:111`) and reachability is driven by ping instead
(`Console/Commands/Device/PingFtpOnlyDevicesCmd.php:26-45`). The only key read is
`connect.protocol`.

---

## The fallback path

Pro only. Runs **before** the sequences above, then hands off to one of them.

Activated when `connect.fallbackProtocol` is present, differs from `connect.protocol`, and both
are `ssh` or `telnet` (`ProtocolFallbackConnectionManager.php:28,50-55`).

| Step | What happens | Keys driving it | Evidence |
| --- | --- | --- | --- |
| 1 | Decide whether fallback applies | `connect.protocol`, `connect.fallbackProtocol` | `ProtocolFallbackConnectionManager.php:50-55` |
| 2 | Work out the port for the attempt | device override, then `connect.fallbackPort` or `connect.port`, then 22 for ssh or 23 for telnet | `ProtocolFallbackConnectionManager.php:30,70-91` |
| 3 | Probe whether the port is open | `connect.probeTimeout`, falling back to `connect.timeout` then 5, clamped to 1 to 10 | `ProtocolFallbackConnectionManager.php:190-196` |
| 4 | Cache the protocol that answered | none | `ProtocolFallbackConnectionManager.php` |
| 5 | Re-enter the normal dispatcher for that protocol | `connect.protocol` | `MainConnectionManager.php:37-40` |

The verification probe sends `config.exitCmd` but deliberately never sends `config.saveConfig`,
because a probe must not write configuration (`PrimaryProtocolVerifier.php:83-95`).

---

## An annotated session: Cisco IOS over SSH with enable

Using `cisco/cisco-ios-ssh-enable.yml`. Wire events on the left, the key that drives each on the
right.

```
WIRE                                            DRIVEN BY
----------------------------------------------  ------------------------------------------
TCP connect to 10.0.0.1:22                      connect.port: 22
  (30 second budget)                            connect.timeout: 30

SSH transport and key exchange                  (library)

Authenticate as the device username             auth.sshPrivKey absent, so password auth
                                                credentials come from the device record,
                                                never from the template

  (hpAnyKeyStatus is off, so no nudge is sent)  auth.hpAnyKeyStatus: off
  (sshInteractive absent, library login used)   auth.sshInteractive not set
  (no vt100 section, no splash handling)        vt100 absent
  (isMikrotik absent, no banner sync)           config.isMikrotik not set

read  until "Password:"                         auth.enablePassPrmpt: "Password:"
                                                reached via the enable branch below

--- enable branch, because enable is on ---     auth.enable: on

read  until the device enable prompt            device record, not the template
write "enable"                                  auth.enableCmd: "enable"
  (enableUsername not set, so no username step) auth.enableUsername not set
read  until "Password:"                         auth.enablePassPrmpt: "Password:"
write <enable password>                         device record
read  until the device main prompt              device record

write "terminal length 0"                       config.pagingCmd, sent because
read  until the device main prompt              config.paging: on

write newline, read to prompt                   (end of enable sequence)

  (syncToPromptOnLogin not set, no drain)       config.syncToPromptOnLogin not set

--- per command, from the Command Group ---

write "show running-config"                     NOT from the template. Commands attach to
read  until the device main prompt              the device through Command Groups.
                                                Read strategy is the standard path, because
                                                sshPrivKey, isNonInteractiveMode, AnsiHost
                                                and isMikrotik are all unset.

--- teardown ---

write "terminal length 40"                      config.resetPagingCmd, sent because
read  until the device main prompt              config.paging: on

disconnect                                      (socket close)
```

Read that last block carefully. The session ends at `disconnect`.

**`saveConfig: "wr mem"` is never sent. `exitCmd: "quit"` is never sent.** Both keys are present
in this template, both are read into memory at step 1, and neither reaches the device, because
this is an SSH session. Move the same two lines into a telnet template and they fire at teardown.

---

## The same stages, three different shapes

The sequence never changes. What changes is which steps do real work.

### Fortinet with a login banner

`fortinet/fortinet-fortios-ssh-noenable-banner.yml` sets `enable: off`, so the enable branch at
step 12a is skipped entirely and step 12b sends the paging command directly. The interesting work
happens earlier, at step 10: the template carries a `vt100` section with
`hasSplashScreen: "on"`, which makes rConfig read up to the banner text and send a control code
to get past it before any prompt matching begins. Without that step the login would appear to
hang, because rConfig would be looking for a username prompt while the device is still displaying
a banner. Note also that the paging command here is multi-line
(`config system console`, `set output standard`, `end`), which is fine: the value is sent as
written at step 12b.

### pfSense escaping the menu

`pfsense/pfsense-ssh-noenable.yml` uses the same stages but bends step 12b into something that is
not really a paging command at all. pfSense presents a numbered console menu after login, and
option 8 drops to a shell. The template sets `pagingCmd: "8"`, so at the point where rConfig
would normally disable paging it instead sends the single character that escapes the menu. This
works because step 12b sends whatever is in `pagingCmd` and then reads to the prompt, which is
exactly the interaction the menu needs. `resetPagingCmd` is empty, so nothing is undone at
step 16.

### MikroTik and the username suffix

`mikrotik/mikrotik-routeros-ssh-noenable.yml` sets `isMikrotik: yes`, which switches on work at
two separate stages. At step 11 rConfig drains the RouterOS banner and sends one Enter to get
past "press Enter to continue". At step 14 it blanks the device prompt entirely and reads with a
match-anything pattern, because RouterOS does not present a stable prompt that regex matching can
rely on. Note that `paging: off` on this template, so step 12b never sends `pagingCmd` despite a
value being present.

MikroTik also needs something the template cannot express at all: the device username must carry
a suffix so RouterOS disables its interactive console features. That is configured on the device
record in rConfig, not in the template, and it is documented in
[mikrotik/README.md](../mikrotik/README.md). If the suffix is missing, every stage above still
runs correctly and the output is still unusable.

---

## Debugging by stage

Find the symptom, get the stage, check those keys first.

| Symptom | Stage it fails at | Keys to check |
| --- | --- | --- |
| No connection at all, immediate failure | 2 to 3, socket open | `connect.port`, `connect.protocol`, and any device port override. Remember the dispatcher matches `protocol` case sensitively, so `SSH` is not `ssh` |
| Connects, then hangs before any login prompt | 10, splash screen | `vt100.hasSplashScreen`, `vt100.splashScreenReadToText`, `vt100.splashScreenSendControlCode`. On SSH also `vt100.hasSplashScreenEnterKey`. A device showing a banner with no `vt100` section will hang here |
| Connects, then hangs on a MikroTik | 11, banner sync | `config.isMikrotik`. Also confirm the username suffix on the device record |
| Login fails or reports the wrong prompt | 7, authenticate | `auth.username`, `auth.password` as prompt patterns, plus the device main prompt on the device record. For key based auth, `auth.sshPrivKey` and the credential set attached to the device |
| Login succeeds on SSH but times out waiting for a prompt | 9, interactive login | `auth.sshInteractive`. Some devices need the manual read and write login rather than the library one |
| Enable mode fails or hangs | 12a | `auth.enable`, `auth.enableCmd`, `auth.enablePassPrmpt`, and the device enable prompt on the device record. If the device asks for a username at enable time, `auth.enableUsername` and `auth.enableUsernamePrmpt`, which are SSH only |
| Enable appears to be ignored | 12a | `auth.enable` must be the string `on`. Check you have not written a YAML boolean |
| Output is truncated, or full of `--More--` and paging prompts | 12a or 12b, paging | `config.paging` and `config.pagingCmd`. On SSH, `paging` must be the string `on` or the command is never sent. On telnet the command is always sent, so a truncation problem there is the command itself being wrong |
| Output is full of escape codes and cursor junk | 14 to 15, read strategy | `options.AnsiHost` set to `yes`, and `options.setTerminalDimensions` for large configurations. On HP, `auth.hpAnyKeyStatus` also selects a scrubbing path |
| Output appears under the wrong command, everything shifted by one | 13, prompt sync | `config.syncToPromptOnLogin` set to `on`, and `config.promptSyncTimeout` if the device is slow. Pro only |
| A command that returns a single line comes back empty | 15, output cleaning | Not a template problem. rConfig drops the first and last line of every response, on the assumption they are the echoed command and the trailing prompt. A one-line response has nothing left after that. Use a command that returns more than one line, or capture it another way |
| Sessions are left open on the device | 11, teardown, telnet only | `config.exitCmd`. On SSH neither `exitCmd` nor `saveConfig` is ever sent, so a device that needs an explicit logout cannot get one over SSH |
| Configuration is not being saved | 10, teardown, telnet only | `config.saveConfig`. Same limitation as above: SSH reads the key and never sends it |
| Paging is never restored | 16 on SSH, 9 on telnet | `config.resetPagingCmd`. On SSH it only fires when `config.paging` is `on`; on telnet it fires whenever the value is not empty |
| Prompt matching works on SSH but not telnet | 8, per command read | Fixed in V8.3.2: telnet now escapes its `/` delimiter, as SSH does for `~`, and Core also tries a literal tail match so plain-text prompts containing regex metacharacters work. On earlier releases a device prompt containing `/` breaks the telnet match |

---

## How this document gates new keys

A new template key is a change to rConfig itself, not to this repository, and the first question
asked of any request is where in the sequence above the new behaviour has to happen. Naming that
point is what makes a request reviewable: it says which manager class changes, which existing
keys the new one interacts with, and whether the behaviour is possible on one protocol or all of
them. A request that cannot name its step is not ready, because there is nowhere to put the code.
Work through the stage tables above, then follow the request process in
[TEMPLATES.md](TEMPLATES.md#requesting-a-new-key).

---

## Verification record

Sequences reconstructed from a full read of the rConfig connection stack in both editions.

| | |
| --- | --- |
| Compiled | 2026-08-16 |
| rConfig Pro analysed | V8.3.2, commit `832e530` |
| rConfig Core analysed | branch `develop`, commit `cdcb518`, app version 8.2.15 |

Core runs the SSH and telnet sequences only. TL1, script, the FTP short circuit and the fallback
path are Pro. Line references are accurate as of those commits and will drift as the code
changes.
