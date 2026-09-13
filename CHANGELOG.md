# Changelog

All notable changes to the rConfig connection template library are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

A major version here means paths changed. Every rename and deletion is mapped in
[docs/MIGRATION.md](docs/MIGRATION.md).

## [Unreleased]

### Added
- `extreme/extreme-nos-ssh-noenable.yml`, for the Brocade derived NOS and SLX-OS CLIs, which
  disable paging with `terminal length 0` rather than the EXOS `disable clipaging`.
- `extreme/README.md`, explaining which of the two Extreme templates to use and how to tell the
  families apart.
- `juniper/juniper-junos-ssh-noenable-kex.yml`, adding the new `kexOverride` /
  `kexAlgorithms` connect keys to force a legacy KEX algorithm list for JunOS devices
  that don't negotiate cleanly against phpseclib's modern defaults.
- **Infinera DTN-X TL1 templates** (`infinera/infinera-dtnx-tl1-ssh.yml`,
  `infinera/infinera-dtnx-tl1-telnet.yml`) and an `infinera/README.md`. A DTN-X presents `>`
  rather than `<`, pages its neighbour response, and answers a routed command under its own
  system name instead of the TID addressed. All three break assumptions carried over from Ciena.
- **Cisco ONS 15454 TL1 templates** (`cisco/cisco-ons15454-tl1-ssh.yml`,
  `cisco/cisco-ons15454-tl1-telnet.yml`), shipped `untested-starter`. Built from the Cisco ONS
  SONET TL1 Command Guide R9.1 and Oracle's TL1 reference, **not from a session capture**. Its
  records are positional rather than keyword-based, and it is the one TL1 platform that reports a
  real model per element.
- **`connect.tl1Vendor`**, the 48th key: `ciena` (default), `infinera` or `cisco-ons`. Selects the
  neighbour verb, the record format, the prompt, and whether a routed reply's SID can be verified.
  An unrecognised value fails the collection rather than falling back.
- **`docs/TL1.md`**, a vendor-neutral guide to TL1: in-band login, gateways and dual-homed
  elements, connection limits, and a table of what actually differs between the three platforms.
- `cisco/README.md` rewritten from 15 lines of caveats into a full template table, the ONS 15454
  section, and the existing FTD and WLC guidance with its typos fixed.

### Changed
- **The "TL1 templates live in `ciena/`" exception is gone.** TL1 templates live with their
  vendor, like every other template here, which makes `cisco/` a mixed-edition directory.
  Edition follows the capability a template uses, never the directory. Restated in
  `docs/EDITIONS.md` and `pro-features/README.md`.
- Ciena templates now carry `tl1Vendor: ciena` and no longer set `tl1NeighbourCmd`. The old
  default, `RTRV-NBR:ALL`, named a command no shipped node answers; each vendor's real command is
  the default now. rConfig substitutes it and logs a warning for templates still naming the old
  verb.
- `ciena/README.md` keeps only what is Ciena-specific. The shared TL1 concepts it used to state as
  universal moved to `docs/TL1.md`.
- `scripts/validate_templates.py` now requires a vendor template's filename to start with its
  directory name. Every file in the library already did; it is worth enforcing now that one
  protocol spans three vendor directories.
- Key counts corrected to 48 across `docs/TEMPLATES.md`, `docs/EDITIONS.md`,
  `docs/CONTRIBUTING.md` and `README.md`, which disagreed with each other at 47/13/14.
- README badges corrected to 38 vendors and 74 templates. The template count was already one
  short before this change.

## [2.0.0] - 2026-08-16

The 2026 restructure. **Every template path changed.** Pin a tag rather than tracking a branch,
and consult `docs/MIGRATION.md` for old path to new path.

The `master` branch is frozen at the pre-restructure tree so existing baked-in URLs keep
resolving. It will not receive further updates.

### Added
- `docs/TEMPLATES.md`, the complete key legend. All 46 keys across 7 sections, verified against rConfig Pro V8.3.2 and Core 8.2.15 source.
- `docs/ORDER-OF-OPERATIONS.md`, when each key fires during a session, per protocol, with a symptom-to-stage debugging table.
- `docs/CONTRIBUTING.md`, naming, headers, content rules and submission.
- `docs/EDITIONS.md`, the Core and Pro support matrix.
- `docs/MIGRATION.md`, old path to new path for every rename and deletion.
- 9 starter templates across 7 new vendor directories: a10, alcatel-lucent, arista, f5, nokia, opengear, zyxel.
- `pro-features/sie/workflows/`, four worked Script Integration Engine examples covering REST backup, change snapshots, multi-step export and database dumps.
- `pro-features/xftp/`, xFTP documentation and device-side push command starters for nine platforms.
- `scripts/validate_templates.py`, enforces the legend in CI. Zero errors required.
- `scripts/apply_headers.py`, idempotent standard header tooling.
- Issue forms for new key requests and template test reports.
- A standard 7-line header on every template, recording edition, verification status, tested-on versions and the filename it replaced.

### Changed
- All vendor directories are lowercase. 25 directories renamed.
- All templates follow `<vendor>-<osfamily>[-<versionqualifier>]-<protocol>-<authmode>[-<variant>].yml`.
- `base/` moved to `_base/` so the starter sorts above the vendor listing.
- Pro-only material consolidated under `pro-features/`.
- `Mellanox/` merged into `nvidia/`. The Onyx template keeps `(Mellanox)` in its display name.
- Display names and descriptions corrected to match template content and the naming convention.
- All files use LF line endings, enforced by `.gitattributes`.

### Fixed
- Two templates were missing the mandatory `auth.hpAnyKeyStatus` key and raised `Undefined array key` at connect time: `hp/hp-comware-ssh-noenable.yml` and `palo-alto/palo-alto-panos-ssh-enable-vector.yml`.
- Five templates whose filename contradicted their content now follow the content.
- `pro-features/sie/*` templates carry `idletimeout` alongside `idleTimeout`, so the value rConfig reads is no longer the hard-coded default.

### Removed
- Deprecated `pagerPrompt` and `pagerPromptCmd` from all templates.
- Keys no code reads: `connect.ctrlYLogin` and a misplaced `auth.linebreak`.
- Two superseded v1 templates, `mikrotik-ssh-noenable.yml` and `panos-ssh.yml`.
