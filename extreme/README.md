# Extreme Networks

Covers the two Extreme CLI families that differ in how paging is turned off.

| Template | Use for |
| --- | --- |
| `extreme-exos-ssh-noenable.yml` | EXOS devices, for example Summit and X series switches |
| `extreme-nos-ssh-noenable.yml` | NOS devices, the Brocade derived VDX and SLX lines |

Neither family uses an enable mode, so both templates connect with `enable: off`.

## Which Extreme template to use

The two families take different paging commands, and sending the wrong one leaves paging on.
The retrieval then stalls at the pager prompt and the saved config is truncated at the first
page.

`extreme-exos-ssh-noenable.yml` sends `disable clipaging`, the EXOS command. This is the
starting point for anything running EXOS.

`extreme-nos-ssh-noenable.yml` sends `terminal length 0`, the Cisco style command that the
Brocade derived NOS and SLX-OS CLIs accept instead. Switch to it if the session log shows an
invalid command error on `disable clipaging`, or if the retrieved config stops after roughly
one screen.

If you are unsure which family a device runs, log in by hand and type `show version`. EXOS
reports an EXOS image, NOS and SLX-OS report a Network OS or SLX-OS version.

Typical retrieval command to attach in an rConfig Command Group:

```text
show running-config
```

`extreme-nos-ssh-noenable.yml` is an untested starter. If you run it against real hardware,
please file a
[template test report](https://github.com/rconfig/rConfig-templates/issues/new?template=template-test-report.yml) so it can be promoted to community-tested.

See [docs/TEMPLATES.md](../docs/TEMPLATES.md) for what each key means and
[docs/CONTRIBUTING.md](../docs/CONTRIBUTING.md) before submitting a change.
