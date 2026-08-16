<a name="readme-top"></a>
<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/rconfig/rconfig">
    <img src="https://portal.rconfig.com/images/rconfig-logos/rConfig-logo-and-icon/rconfig_logo_and_icon_with_strapline_gradient.png" alt="rConfig Logo" width="500"/>
  </a>

  <h3 align="center">rConfig - Templates</h3>

  <!-- Shields.io badges -->
  <p align="center">
    <img src="https://img.shields.io/badge/vendors-40-blueviolet?style=for-the-badge&logo=yaml&logoColor=white" alt="Vendors Badge"/>
    <img src="https://img.shields.io/badge/templates-71-blue?style=for-the-badge&logo=yaml&logoColor=white" alt="Templates Badge"/>
  </p>

  <p align="center">
    Community connection templates for <a href="https://www.rconfig.com">rConfig</a> V8 Core and Pro.
  </p>
</div>
<br>

## Quick start

1. **Find your vendor directory**, or copy `_base/base.yml` if your vendor is not here yet.
2. **Import the template into rConfig**, then assign it to the device.
3. **Attach your retrieval commands to the device in rConfig Command Groups.**

That third step matters, because the split is not obvious: **a template handles the connection,
Command Groups handle the commands.** The template says how to log in, get past the banner, enter
enable mode and turn paging off. It does not say `show running-config`. If you are looking for
where the commands live, they are Command Groups, attached to the device, not the template.

## Documentation

| Document | What it covers |
| --- | --- |
| [docs/TEMPLATES.md](docs/TEMPLATES.md) | The legend. Every key, what it means, what values it takes, which protocols read it |
| [docs/ORDER-OF-OPERATIONS.md](docs/ORDER-OF-OPERATIONS.md) | When each key fires during a session, per protocol, plus debugging by stage |
| [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) | Naming, headers, content rules and how to submit |
| [docs/MIGRATION.md](docs/MIGRATION.md) | Old path to new path for the 2026 restructure |
| [docs/noninteractive-ssh.md](docs/noninteractive-ssh.md) | The SSH non-interactive shell mode |

## Repository layout

```text
_base/            Starter template to copy when adding a new vendor
<vendor>/         One directory per vendor, holding its templates and a README
pro-features/     Pro-only material: sie/, ssh-private-key/, xftp/
docs/             The legend, order of operations, contributing guide, migration map
scripts/          Header tooling and the template validator
.github/          Issue forms and the validation workflow
```

Pro-only material lives under `pro-features/`: the Script Integration Engine templates and
example scripts, the SSH private key template, and the xFTP inbound-only template.

## Template status

Every template declares a status in its header.

| Status | Meaning |
| --- | --- |
| `rconfig-verified` | Tested by the rConfig team |
| `community-tested` | Someone ran it against real hardware and reported the result |
| `untested-starter` | A best guess at the right shape, not yet run against real hardware |

**12 templates are currently `untested-starter`.** If you have the hardware, running one and
filing a
[template test report](https://github.com/rconfig/rConfig-templates/issues/new?template=template-test-report.yml)
is the single most valuable small contribution you can make here. Reports are welcome whether the
template worked, needed changes, or failed outright.

## Naming

```text
<vendor>-<osfamily>[-<versionqualifier>]-<protocol>-<authmode>[-<variant>].yml
```

Two real examples from this repository:

```text
cisco/cisco-ios-ssh-enable.yml
cisco/cisco-ios-telnet-noenable.yml
```

The vendor prefix repeats the directory name deliberately, because filenames travel without their
paths. See [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) for the full rules, including when a
hardware model belongs in the filename and when it does not.

## Template keys

This README carries no key documentation. The full reference lives in
[docs/TEMPLATES.md](docs/TEMPLATES.md): 46 keys across 7 sections, each with its type, accepted
values, default, and which protocols read it.

If your device needs behaviour no existing key can express, open a
[new key request](https://github.com/rconfig/rConfig-templates/issues/new?template=new-key-request.yml).

## Community

- Open an [issue](https://github.com/rconfig/rConfig-templates/issues) for a bug, a question, or a template request
- Join the [rConfig community](https://rconfig.com/community/)
- Browse the [rConfig documentation](https://docs.rconfig.com/)

Thanks for helping grow the rConfig community. Every template here came from someone who had the
hardware in front of them and took the time to write it down.
