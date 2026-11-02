# SonicWall

Covers SonicOS over SSH. The templates differ in how the device logs you in.

| Template | Use for |
| --- | --- |
| `sonicwall-sonicos-ssh-noenable.yml` | Devices that ask for the username and password before the session opens |
| `sonicwall-sonicos-ssh-enable-banner.yml` | The same, where a login banner must be confirmed with `yes` |
| `sonicwall-sonicos-ssh-noenable-nousername.yml` | Devices that ask for the password inside the session, with no username prompt |

## In-band password login

Some SonicOS devices accept the SSH connection without checking the password, then ask for it
inside the session:

```text
Using username 'rconfbackup'.
Password:
```

To check, connect by hand with `ssh <user>@<device>`. If the password is requested after the
`Using username` line rather than by your SSH client, use
`sonicwall-sonicos-ssh-noenable-nousername.yml`. It logs in at that prompt and sends only the
password.

With the other SonicWall templates these devices take every command as a password attempt. The
debug output (`php artisan rconfig:download-device <id> -d`) shows `Access denied` after each
command. From rConfig Pro V8.4.2 the download is reported as a failed login. Earlier versions save
`Access denied` as the config and report success.

**Requires rConfig Pro V8.4.2 or later.** Older versions and Core always send the username first,
so it is taken as a wrong password before the real password goes through. The backup still
works, but the device logs one failed login for every backup. Check the device's failed-login
lockout settings before using it on those versions.

Typical retrieval command to attach in an rConfig Command Group:

```text
show current-config
```

`sonicwall-sonicos-ssh-noenable-nousername.yml` is an untested starter. If you run it against real
hardware, please file a
[template test report](https://github.com/rconfig/rConfig-templates/issues/new?template=template-test-report.yml) so it can be promoted to community-tested.

See [docs/TEMPLATES.md](../docs/TEMPLATES.md) for what each key means and
[docs/CONTRIBUTING.md](../docs/CONTRIBUTING.md) before submitting a change.
