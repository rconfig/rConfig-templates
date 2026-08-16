# Device-side push commands

Starter commands for telling a device to push its configuration to rConfig's inbound file service.

**Every command here is a starter to verify, not a drop-in.** Syntax varies by platform version,
and several of these differ between minor releases. Test against one device before rolling any of
them out.

Behaviour described here was verified against rConfig Pro 8.3.2.

## Read this before using placeholders

rConfig substitutes placeholder variables into device commands, but **only five of them**:

| Placeholder | Substituted into device commands |
| --- | --- |
| `{deviceid}` | Yes |
| `{ftpusername}` | Yes |
| `{ftppassword}` | Yes |
| `{sftpusername}` | Yes |
| `{sftppassword}` | Yes |
| `{device_ip}` | **No** |
| `{device_name}` | **No** |
| `{device_username}` | **No** |
| `{device_password}` | **No** |
| `{device_enable_password}` | **No** |
| `{script_path}` | **No** |

The second group exists in rConfig but is **not** substituted on the SSH or telnet command path.
Putting `{device_name}` in a command sends the literal text `{device_name}` to the device.

Only the five in the first group are safe to use in the commands below.

Substitution happens on SSH and telnet commands. It does not apply to Script Integration Engine
scripts, which take their inputs from the environment instead.

## The server placeholder

Replace `<rconfig-server>` with your rConfig host's address. It is written as a placeholder here
because rConfig does not substitute it for you.

## Naming the file

Start the filename with `{deviceid}` and a hyphen. That is the fallback the sweeper looks for when
no file matching rule is configured, so it works out of the box:

```text
{deviceid}-something.cfg     ->  12345-something.cfg
```

If you need a different naming scheme, configure a file matching rule for the device instead. See
the [README](../README.md).

---

## Cisco IOS

```text
copy running-config ftp://{ftpusername}:{ftppassword}@<rconfig-server>/{deviceid}-running-config.cfg
```

SCP over SSH, if the device is configured for it:

```text
copy running-config scp://{sftpusername}:{sftppassword}@<rconfig-server>/{deviceid}-running-config.cfg
```

IOS normally prompts to confirm the destination. Suppress the prompts with `file prompt quiet` in
configuration mode, or the copy will sit waiting for a keystroke that never comes.

## Cisco NX-OS

```text
copy running-config sftp://{sftpusername}@<rconfig-server>/{deviceid}-running-config.cfg vrf management
```

The `vrf` keyword is usually required on NX-OS, and the VRF name is often but not always
`management`. NX-OS prompts for the password interactively on SFTP; if that blocks you, use FTP:

```text
copy running-config ftp://{ftpusername}:{ftppassword}@<rconfig-server>/{deviceid}-running-config.cfg vrf management
```

## Cisco ASA

```text
copy /noconfirm running-config ftp://{ftpusername}:{ftppassword}@<rconfig-server>/{deviceid}-running-config.cfg
```

`/noconfirm` matters here. Without it the ASA asks for confirmation and the command stalls.

## Fortinet FortiGate

```text
execute backup config ftp {deviceid}-fgt-config.conf <rconfig-server> {ftpusername} {ftppassword}
```

FortiGate takes the arguments positionally rather than as a URL. On a VDOM-enabled unit run this
from the global context, or you will back up one VDOM instead of the whole device.

## F5 BIG-IP

Two steps: build the UCS archive, then upload it. A UCS is a binary archive rather than text, so
this is exactly the case xFTP exists for.

```text
tmsh save sys ucs /var/tmp/{deviceid}-backup.ucs

curl -T /var/tmp/{deviceid}-backup.ucs \
  ftp://<rconfig-server>/{deviceid}-backup.ucs \
  --user {ftpusername}:{ftppassword}
```

The second command runs from the bash shell, not from tmsh. Clean up `/var/tmp` afterwards or the
archives accumulate.

## Palo Alto PAN-OS

```text
scp export configuration from running-config.xml to {sftpusername}@<rconfig-server>:{deviceid}-running-config.xml
```

PAN-OS prompts for the password and, on a first connection, to accept the host key. Accept the key
once manually from the CLI before relying on this.

## Juniper Junos

```text
file copy /config/juniper.conf.gz ftp://{ftpusername}:{ftppassword}@<rconfig-server>/{deviceid}-juniper.conf.gz
```

For plain text rather than the compressed active configuration:

```text
show configuration | save /var/tmp/{deviceid}-config.txt
file copy /var/tmp/{deviceid}-config.txt ftp://{ftpusername}:{ftppassword}@<rconfig-server>/{deviceid}-config.txt
```

Junos can also do this on a schedule with `system archival configuration`, which is worth
considering instead of driving it from rConfig.

## HP and Aruba ProCurve

```text
copy running-config tftp <rconfig-server> {deviceid}-running-config.cfg
```

ProCurve's TFTP support is the most reliable option on this platform, and TFTP is unauthenticated.
Only do this on an isolated management network.

Newer AOS-Switch firmware supports SFTP, which is the better choice where available:

```text
copy running-config sftp {sftpusername}@<rconfig-server> {deviceid}-running-config.cfg
```

## MikroTik RouterOS

```text
/export file={deviceid}-export
/tool fetch address=<rconfig-server> src-path={deviceid}-export.rsc \
  user={ftpusername} password={ftppassword} upload=yes mode=ftp
```

`/export` writes `{deviceid}-export.rsc` to the device's own storage first, so the fetch has
something to send. The `.rsc` extension is added by RouterOS and must appear in `src-path`.

Remember the `+cte` username suffix RouterOS needs for rConfig sessions, documented in
[mikrotik/README.md](../../../mikrotik/README.md). It applies to the connection, not to this
command.

---

## Once the file arrives

The sweeper picks it up on its next run and files it against the device. If a file is not being
matched, check the filename against the rules in the [README](../README.md): the device ID
fallback needs the ID at the start followed by a hyphen, or preceded by `device`, `dev` or `id`.
