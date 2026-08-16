# Contributing a template

How to add or change a connection template in this repository.

A connection template describes how rConfig talks to a device. It does not hold the commands
whose output you want to capture: those attach to devices through Command Groups.

Related reading:

- [TEMPLATES.md](TEMPLATES.md) - every key, what it means, what values it takes
- [ORDER-OF-OPERATIONS.md](ORDER-OF-OPERATIONS.md) - when each key fires during a session
- [MIGRATION.md](MIGRATION.md) - old path to new path for the 2026 restructure
- [CLAUDE.md](../CLAUDE.md) - the repository standards this document reproduces

---

## 1. Naming your file

```text
<vendor>-<osfamily>[-<versionqualifier>]-<protocol>-<authmode>[-<variant>].yml
```

| Token | Required | What it is |
| --- | --- | --- |
| `vendor` | yes | Matches the directory name |
| `osfamily` | usually | The OS or CLI family, never a hardware model. Omit only when the vendor has a single uniform CLI |
| `versionqualifier` | no | Only where the vendor has real version differences in connection behaviour. Example: `panos-9x` |
| `protocol` | yes | `ssh` or `telnet`. `script` and `tl1` exist for Pro templates |
| `authmode` | usually | `enable` or `noenable`, with `nousername` as an additional variant where relevant |
| `variant` | no | Agent or mode specifics such as `vector`, `noninteractive`, `banner`, `vdom` |

All lowercase, hyphens only, no underscores or spaces.

**The vendor prefix repeats the directory name on purpose.** Filenames travel without their
paths through downloads, imports and attachments, so they have to be self-identifying.
`cisco/cisco-ios-ssh-enable.yml` is correct, not `cisco/ios-ssh-enable.yml`.

**Hardware models appear only when the model itself changes connection behaviour.** The example
to reason from is `hp-1920-ssh-enable.yml`: the 1920 keeps its model number because it requires
a special elevation command that other HP switches do not. A model number that only tells you
what was on the bench when the template was written does not belong in the filename. Record that
in `Tested-on` instead.

**Variants may chain** when a template genuinely carries more than one, as in
`mikrotik-routeros-ssh-noenable-noninteractive-vector.yml`.

**`authmode` is omitted for protocols with no enable concept**, which means `tl1` and `script`.
`ciena-6500-tl1-ssh.yml` is complete as it stands.

---

## 2. The header

Every template opens with this block. `scripts/apply_headers.py` generates it, and the script is
idempotent, so run it rather than hand-writing the header.

```text
# rConfig connection template
## Edition: <core|pro>
## Status: <rconfig-verified|community-tested|untested-starter>
## Tested-on: <rConfig versions and editions the template is known to work on>
## Replaces: <old filename, renamed templates only>
## Docs: <documentation URL>
## Community: https://github.com/rconfig/rConfig-templates
## Note: all free-text values must be wrapped in double quotes " "
```

Seven lines, or eight when `Replaces` is present.

| Field | Rule |
| --- | --- |
| `Edition` | Content-aware, not a choice. `pro` when the protocol is `script`, `tl1` or `xftp`, or when the template uses `sshPrivKey`. Everything else is `core` |
| `Status` | See the lifecycle below |
| `Tested-on` | The rConfig versions and editions you actually saw it work on. Not aspirational |
| `Replaces` | Only on templates renamed during the 2026 restructure, sourced from `MIGRATION.md`. A new template has no `Replaces` line |
| `Docs` | The Script Integration Engine URL for `script` protocol templates, the connection templates URL for everything else |
| `Community` | Always the repository URL, unchanged |
| `Note` | Always the quoting reminder, unchanged |

Vendor specific comments belong immediately below the header. `apply_headers.py` preserves them
and re-emits them there, so put device quirks in a `##` comment rather than losing them in a
commit message.

---

## 3. Status lifecycle

```text
untested-starter  ->  community-tested  ->  rconfig-verified
```

**`untested-starter`** is where a new template begins if you are contributing a shape you believe
is right but have not run against real hardware, or have run only against a simulator. It is a
legitimate contribution: an honest starter beats no template at all, and it tells the next person
exactly how much to trust it.

**`community-tested`** means someone ran it against a real device and reported the result. Most
of this library sits here. Moving a template from starter to community-tested needs a test report
saying which device, which OS version, which rConfig version, and what was captured.

**`rconfig-verified`** is reserved for templates the rConfig team has tested themselves. Do not
set it on a contribution. If your template earns it, the team will change it.

Use the [template test report form](../.github/ISSUE_TEMPLATE/template-test-report.yml), which
asks for each of those details in turn. Reports are welcome whether the template worked, needed
changes, or failed outright.

Never lower a status without saying why, and never raise one without evidence.

---

## 4. Content rules

**Quote free text.** Every free-text value goes in double quotes. Prompts, commands and
descriptions all count.

**Use `on` and `off`, never `true` and `false`.** This is the single most common way to break a
template silently. rConfig parses YAML 1.2, where `on` and `off` stay strings but `true` and
`false` become booleans, and the connection code compares against the strings. `paging: true`
does not disable paging and logs nothing. Worse, the failure is not consistent between keys:
`enable: true` does work. Read
[the callout in TEMPLATES.md](TEMPLATES.md#the-onoff-trap-read-this-first) before you write
either value. The validator fails the build on a boolean in `enable`, `paging` or
`hpAnyKeyStatus`.

**ASCII only.** No em dashes, en dashes, curly quotes or emoji, anywhere in the file including
comments. Use the ASCII hyphen.

**LF line endings.** Enforced by `.gitattributes`. If your editor writes CRLF, fix the editor
rather than the file.

**No deprecated keys.** `pagerPrompt` and `pagerPromptCmd` are ignored by rConfig and must not
appear. The validator treats them as errors.

**Only keys in the legend.** [TEMPLATES.md](TEMPLATES.md) lists all 46 keys across 7 sections.
Anything else is an error, because a key rConfig does not read does nothing except mislead the
next reader. If your device needs behaviour no existing key expresses, use the
[new key request form](../.github/ISSUE_TEMPLATE/new-key-request.yml). That is a change to
rConfig itself, so it starts before any pull request here.

**Comment the quirks inline.** If a value looks wrong but is deliberate, say so on the line. The
ProCurve template carries `pagingCmd: "nno page"` with a comment explaining that the doubled
letter is sacrificial, because some HPE firmware swallows the first character after the any-key
prompt. Without that comment someone would have "fixed" it years ago.

---

## 5. A caution about reformatting

As of Pro 8.3.2 and Core 8.2.15, the product's built-in template reformat function does not
preserve the `vt100` and `failure_criteria` sections. Do not run reformat on templates that use
them.

The templates affected today are:

```text
avaya/avaya-ers-ssh-noenable-vector.yml
avaya/avaya-ers-telnet-noenable.yml
fortinet/fortinet-fortios-ssh-noenable-banner.yml
siemens/siemens-ruggedcom-ros-ssh-noenable.yml
SIE-Base/script_template.yml
SIE-Radware/alteon_expect_script_template.yml
```

For everything else, reformat is safe. Run the validator afterwards either way.

---

## 6. Submitting

1. **Fork** this repository and create a branch. Name it for what it does, for example
   `add-juniper-srx-template`.
2. **Write or edit the template.** Put it in the vendor directory that matches its `vendor`
   token, creating the directory if the vendor is new. New directories are lowercase and named
   for the vendor's common short form.
3. **Run the header tool**, which will generate or update the header block in place:
   ```bash
   python3 scripts/apply_headers.py
   ```
4. **Run the validator. Zero errors is required.**
   ```bash
   python3 scripts/validate_templates.py
   ```
   Warnings do not block a merge, but a warning on a file you touched needs a sentence in the
   pull request explaining it. Warnings on files you did not touch are pre-existing and are not
   your problem.
5. **Open a pull request** including:
   - the device, its OS and version
   - which rConfig version and edition you tested against, **matching what you put in
     `Tested-on`**
   - what you captured successfully, and anything that did not work
   - for a fix to an existing template, what was failing before

Both the validator and the header check run in CI on every push and pull request, so a mismatch
will surface whether or not you ran them locally. Running them first is faster.

A pull request whose `Tested-on` claim is not backed by evidence in the description will be asked
for that evidence before review, because the header is a promise to the next person who picks the
template up.
