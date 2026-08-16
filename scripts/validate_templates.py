#!/usr/bin/env python3
"""Validate every rConfig connection template against docs/TEMPLATES.md.

Checks file hygiene, the standard header, the key legend, per-protocol mandatory
keys, deprecated keys, value types and filename convention.

Exit code 0 when clean, 1 when any ERROR is raised. WARN never fails the run.

Usage:
    python3 scripts/validate_templates.py
    python3 scripts/validate_templates.py --quiet    # summary only
"""

import os
import re
import sys

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required. pip install pyyaml", file=sys.stderr)
    sys.exit(1)

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {".git", ".github", "docs", "scripts"}


class RConfigLoader(yaml.SafeLoader):
    """A loader that types scalars the way rConfig does.

    rConfig parses templates with symfony/yaml, which follows YAML 1.2: only
    true and false are booleans, while on, off, yes and no stay strings.
    PyYAML defaults to YAML 1.1, where all of those are booleans. Validating
    with the default loader would report every template as broken and would
    miss the real 'paging: true' mistake, so the bool resolver is narrowed here
    to match the runtime.
    """


RConfigLoader.yaml_implicit_resolvers = {
    ch: [(tag, rx) for tag, rx in resolvers if tag != "tag:yaml.org,2002:bool"]
    for ch, resolvers in yaml.SafeLoader.yaml_implicit_resolvers.items()
}
RConfigLoader.add_implicit_resolver(
    "tag:yaml.org,2002:bool",
    re.compile(r"^(?:true|True|TRUE|false|False|FALSE)$"),
    list("tTfF"),
)

LEGEND = "docs/TEMPLATES.md"
NEW_KEY_PROCESS = "see 'Requesting a new key' in " + LEGEND

# ---------------------------------------------------------------------------
# The legend: 46 keys across 7 sections, from docs/TEMPLATES.md
# ---------------------------------------------------------------------------

ALLOWED = {
    "main": {"name", "desc"},
    "connect": {
        "protocol", "port", "timeout", "isNonInteractiveMode", "idletimeout",
        "sshAuth", "tl1Transport", "tl1Gateway", "tl1NeighbourCmd",
        "fallbackProtocol", "fallbackPort", "probeTimeout",
    },
    "auth": {
        "username", "password", "enable", "enableCmd", "enablePassPrmpt",
        "enableUsername", "enableUsernamePrmpt", "hpAnyKeyStatus",
        "hpAnyKeyPrmpt", "sshInteractive", "sshPrivKey",
    },
    "vt100": {
        "hasSplashScreen", "hasSplashScreenEnterKey", "splashScreenReadToText",
        "splashScreenSendControlCode",
    },
    "config": {
        "paging", "pagingCmd", "resetPagingCmd", "saveConfig", "exitCmd",
        "isMikrotik", "linebreak", "syncToPromptOnLogin", "promptSyncTimeout",
        "pagerPrompt", "pagerPromptCmd",
    },
    "options": {"AnsiHost", "setWindowSize", "setTerminalDimensions"},
    "failure_criteria": {"exit_codes", "error_patterns", "success_patterns"},
}

DEPRECATED = {"config": {"pagerPrompt", "pagerPromptCmd"}}

# Mandatory keys per protocol, as "section.key"
CONNECTION_MANDATORY = [
    "main.name", "main.desc",
    "connect.protocol", "connect.port", "connect.timeout",
    "auth.username", "auth.password", "auth.enable", "auth.enableCmd",
    "auth.enablePassPrmpt", "auth.hpAnyKeyStatus",
    "config.paging", "config.pagingCmd", "config.resetPagingCmd",
    "config.saveConfig", "config.exitCmd", "config.linebreak",
]
MANDATORY = {
    "ssh": CONNECTION_MANDATORY,
    "telnet": CONNECTION_MANDATORY,
    "tl1": ["main.name", "main.desc", "connect.protocol", "connect.port", "connect.timeout"],
    "script": ["connect.protocol"],
    # Inbound-only. xftp is the canonical spelling from V8.3.2, ftp stays accepted for
    # templates already in the field.
    "xftp": ["connect.protocol"],
    "ftp": ["connect.protocol"],
}
KNOWN_PROTOCOLS = set(MANDATORY)

# Keys whose value must be the string "on" or "off", never a YAML boolean.
ONOFF_KEYS = [("auth", "enable"), ("config", "paging"), ("auth", "hpAnyKeyStatus")]

# Header
HEADER_TITLE = "# rConfig connection template"
EDITIONS = {"core", "pro"}
STATUSES = {"rconfig-verified", "community-tested", "untested-starter"}
DOCS_SCRIPT = "https://docs.rconfig.com/integrations/script-integration-engine/sie/"
DOCS_DEFAULT = "https://docs.rconfig.com/device-management/connection-templates/"
COMMUNITY = "https://github.com/rconfig/rConfig-templates"

# Filenames that predate the convention and are handled in a later phase.
FILENAME_EXCEPTIONS = {
    "_base/base.yml",
    "pro-features/sie/_base/script_template.yml",
    "pro-features/sie/radware/radware-alteon-script-template.yml",
    "pro-features/ssh-private-key/ssh-private-key-template.yml",
    "pro-features/xftp/xftp-inbound-only.yml",
}

# ---------------------------------------------------------------------------
# TEMPORARY ALLOWLIST
#
# Each entry is a known deviation with a decision still pending. They are
# reported as WARN so CI stays green while the decision is outstanding.
#
# These become ERRORs when the Phase 5 decisions land: delete the entry and the
# generic unknown-key and protocol-value checks below will fail the file.
# ---------------------------------------------------------------------------
# connect.ctrlYLogin and auth.linebreak were removed from their templates in P5.7. Their
# allowlist entries are gone with them, so the generic unknown-key check now ERRORs if either
# is reintroduced.
ALLOWLIST_KEYS = {
    ("pro-features/sie/_base/script_template.yml", "connect", "idleTimeout"):
        "camelCase kept for forward compatibility alongside the lowercase idletimeout the code "
        "reads. Remove this entry when the product accepts both spellings",
    ("pro-features/sie/radware/radware-alteon-script-template.yml", "connect", "idleTimeout"):
        "camelCase kept for forward compatibility alongside the lowercase idletimeout the code "
        "reads. Remove this entry when the product accepts both spellings",
}
# xftp became a recognised protocol value in V8.3.2, so it no longer needs an allowlist
# entry. Kept as an empty map because entries may be needed again for a future value.
ALLOWLIST_PROTOCOLS = {}


class Report:
    def __init__(self):
        self.errors = []
        self.warnings = []

    def error(self, path, msg):
        self.errors.append(f"ERROR {path}: {msg}")

    def warn(self, path, msg):
        self.warnings.append(f"WARN  {path}: {msg}")


def templates():
    for dirpath, dirnames, filenames in os.walk(REPO):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in sorted(filenames):
            if fn.endswith(".yml"):
                yield os.path.relpath(os.path.join(dirpath, fn), REPO)


def check_hygiene(rel, raw, rep):
    if b"\r\n" in raw or b"\r" in raw:
        rep.error(rel, "CRLF or CR line endings, must be LF")
    try:
        text = raw.decode("ascii")
    except UnicodeDecodeError as e:
        rep.error(rel, f"non-ASCII byte at offset {e.start}")
        text = raw.decode("utf-8", errors="replace")
    if raw and not raw.endswith(b"\n"):
        rep.error(rel, "no trailing newline at end of file")
    return text


def check_header(rel, text, protocol, rep):
    lines = text.split("\n")
    titles = [i for i, l in enumerate(lines) if l.rstrip() == HEADER_TITLE]
    if len(titles) == 0:
        rep.error(rel, f"standard header missing, expected '{HEADER_TITLE}' as line 1")
        return
    if len(titles) > 1:
        rep.error(rel, f"standard header appears {len(titles)} times, expected exactly one")
        return
    if titles[0] != 0:
        rep.error(rel, "standard header must be the first line of the file")

    fields = {}
    for l in lines[:20]:
        m = re.match(r"^##\s*([A-Za-z-]+):\s*(.*?)\s*$", l)
        if m:
            fields.setdefault(m.group(1), m.group(2))

    edition = fields.get("Edition")
    if edition is None:
        rep.error(rel, "header missing '## Edition:'")
    elif edition not in EDITIONS:
        rep.error(rel, f"header Edition '{edition}' invalid, expected one of {sorted(EDITIONS)}")

    status = fields.get("Status")
    if status is None:
        rep.error(rel, "header missing '## Status:'")
    elif status not in STATUSES:
        rep.error(rel, f"header Status '{status}' invalid, expected one of {sorted(STATUSES)}")

    tested = fields.get("Tested-on")
    if tested is None:
        rep.error(rel, "header missing '## Tested-on:'")
    elif tested == "":
        rep.error(rel, "header Tested-on is empty")

    docs = fields.get("Docs")
    want = DOCS_SCRIPT if protocol == "script" else DOCS_DEFAULT
    if docs is None:
        rep.error(rel, "header missing '## Docs:'")
    elif docs != want:
        rep.error(rel, f"header Docs should be {want} for protocol '{protocol}', found {docs}")

    if fields.get("Community") != COMMUNITY:
        rep.error(rel, f"header missing or wrong '## Community:', expected {COMMUNITY}")
    if "Note" not in fields:
        rep.error(rel, "header missing '## Note:'")


def check_keys(rel, doc, rep):
    for section, body in doc.items():
        if section not in ALLOWED:
            rep.error(rel, f"unknown section '{section}', {NEW_KEY_PROCESS}")
            continue
        if not isinstance(body, dict):
            rep.error(rel, f"section '{section}' is not a mapping")
            continue
        for key in body:
            if key in DEPRECATED.get(section, set()):
                rep.error(rel, f"deprecated key '{section}.{key}' must be removed")
                continue
            if key in ALLOWED[section]:
                continue
            why = ALLOWLIST_KEYS.get((rel, section, key))
            if why:
                rep.warn(rel, f"allowlisted key '{section}.{key}': {why}")
            else:
                rep.error(rel, f"unknown key '{section}.{key}', {NEW_KEY_PROCESS}")


def check_mandatory(rel, doc, protocol, rep):
    for dotted in MANDATORY.get(protocol, []):
        section, key = dotted.split(".", 1)
        if key not in (doc.get(section) or {}):
            rep.error(rel, f"missing mandatory key '{dotted}' for protocol '{protocol}'")


def check_values(rel, doc, rep):
    for section, key in ONOFF_KEYS:
        if key not in (doc.get(section) or {}):
            continue
        v = doc[section][key]
        if isinstance(v, bool):
            rep.error(
                rel,
                f"'{section}.{key}' is a YAML boolean, must be the string on or off. "
                f"Unquoted true and false become booleans and are compared inconsistently",
            )
        elif v not in ("on", "off"):
            rep.error(rel, f"'{section}.{key}' is {v!r}, expected the string on or off")


def check_filename(rel, rep):
    if rel in FILENAME_EXCEPTIONS:
        return
    base = os.path.basename(rel)
    if not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*\.yml$", base):
        rep.error(rel, f"filename '{base}' is not lowercase-hyphenated, see CLAUDE.md")


def main():
    quiet = "--quiet" in sys.argv
    rep = Report()
    names = {}
    files = sorted(templates())

    for rel in files:
        raw = open(os.path.join(REPO, rel), "rb").read()
        text = check_hygiene(rel, raw, rep)
        check_filename(rel, rep)

        try:
            doc = yaml.load(text, Loader=RConfigLoader)
        except yaml.YAMLError as e:
            rep.error(rel, f"invalid YAML: {str(e).splitlines()[0]}")
            continue
        if not isinstance(doc, dict):
            rep.error(rel, "top level of the file is not a mapping")
            continue

        protocol = (doc.get("connect") or {}).get("protocol")
        protocol = str(protocol).lower() if protocol is not None else None

        if protocol is None:
            rep.error(rel, "missing 'connect.protocol'")
        elif protocol not in KNOWN_PROTOCOLS:
            why = ALLOWLIST_PROTOCOLS.get((rel, protocol))
            if why:
                rep.warn(rel, f"allowlisted protocol '{protocol}': {why}")
            else:
                rep.error(
                    rel,
                    f"unknown protocol '{protocol}', expected one of {sorted(KNOWN_PROTOCOLS)}",
                )

        check_header(rel, text, protocol, rep)
        check_keys(rel, doc, rep)
        if protocol in MANDATORY:
            check_mandatory(rel, doc, protocol, rep)
        check_values(rel, doc, rep)

        name = (doc.get("main") or {}).get("name")
        if name:
            names.setdefault(name, []).append(rel)

    for name, where in sorted(names.items()):
        if len(where) > 1:
            rep.error(where[0], f"main.name {name!r} is not unique, also in {', '.join(where[1:])}")

    if not quiet:
        for line in rep.errors:
            print(line)
        for line in rep.warnings:
            print(line)
        if rep.errors or rep.warnings:
            print()

    print(f"{len(files)} templates checked, {len(rep.errors)} errors, {len(rep.warnings)} warnings")
    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main())
