#!/usr/bin/env python3
"""Apply the standard rConfig template header to every connection template.

Idempotent. A second run makes no changes. On rerun the existing header's
Status and Tested-on values are preserved, so manual verification results are
never overwritten.

Also normalises line endings to LF.

Usage:
    python3 scripts/apply_headers.py            # apply
    python3 scripts/apply_headers.py --check    # report only, exit 1 if changes needed
"""

import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SKIP_DIRS = {".git", ".github", "docs", "scripts"}

DOCS_SCRIPT = "https://docs.rconfig.com/integrations/script-integration-engine/sie/"
DOCS_DEFAULT = "https://docs.rconfig.com/device-management/connection-templates/"
COMMUNITY = "https://github.com/rconfig/rConfig-templates"
NOTE = 'all free-text values must be wrapped in double quotes " "'

TITLE = "# rConfig connection template"

# Status and Tested-on policy. Keys are repo-relative paths.
BASE_TEMPLATE = "_base/base.yml"
POLICY_BASE = ("rconfig-verified", "rConfig V6, V7 and V8, Core and Pro")
POLICY_LEGACY = ("community-tested", "rConfig V6, V7 and V8")

# Pro directory files. These need human review, see the P3.2 report.
POLICY_PRO = {
    "pro-features/sie/_base/script_template.yml": ("rconfig-verified", "rConfig V8 Pro"),
    "pro-features/sie/radware/radware-alteon-script-template.yml": ("community-tested", "rConfig V8 Pro"),
    "pro-features/ssh-private-key/ssh-private-key-template.yml": ("community-tested", "rConfig V6, V7 and V8"),
    "pro-features/xftp/xftp-inbound-only.yml": ("untested-starter", "rConfig V8"),
}
# TL1 is a Pro only protocol and postdates V6, so the legacy string does not apply.
POLICY_TL1 = ("community-tested", "rConfig V8 Pro")

# Legacy boilerplate. Any pre-main comment line matching one of these is dropped.
# Anything else is a vendor note and is re-emitted below the header.
BOILERPLATE = [
    r"^#\s*rConfig connection template\s*[-–—]\s*DO NOT EDIT DIRECTLY\s*$",
    r"^##\s*Template Notes:\s*$",
    r"^\s*##\s*Notes:\s*$",
    r"^\s*##\s*-?\s*All free text values must be wrapped in double quotes.*$",
    r"^\s*##\s*all items below that contain free text should be contained within quotation marks.*$",
    r"^\s*##\s*-?\s*Documentation:\s*https?://\S+\s*$",
    r"^\s*##\s*-?\s*Community templates and contributions:\s*https?://\S+\s*$",
    r"^\s*##\s*For new community submitted templates visit:\s*https?://\S+\s*$",
    r"^\s*##\s*Remember to update permissions for the templates folder.*$",
    r"^\s*##\s*run 'chown.*$",
    r"^\s*##\s*$",
]
BOILERPLATE_RE = [re.compile(p, re.IGNORECASE) for p in BOILERPLATE]

# Lines belonging to a previously applied standard header.
STD_FIELD_RE = re.compile(
    r"^##\s*(Edition|Status|Tested-on|Replaces|Docs|Community|Note):", re.IGNORECASE
)


def migration_replaces():
    """new basename -> old basename, parsed from docs/MIGRATION.md."""
    path = os.path.join(REPO, "docs", "MIGRATION.md")
    out = {}
    if not os.path.exists(path):
        return out
    row = re.compile(r"^\|\s*`([^`]+\.yml)`\s*\|\s*`([^`]+\.yml)`\s*\|")
    # Only the rename tables count. The Removed section lists superseded files,
    # which are deletions, not renames.
    for line in open(path, encoding="utf-8"):
        if line.startswith("## Removed"):
            break
        m = row.match(line)
        if not m:
            continue
        old, new = m.group(1), m.group(2)
        if os.path.basename(old) != os.path.basename(new):
            out[new] = os.path.basename(old)
    return out


def templates():
    for dirpath, dirnames, filenames in os.walk(REPO):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in sorted(filenames):
            if fn.endswith(".yml"):
                yield os.path.relpath(os.path.join(dirpath, fn), REPO)


UNICODE_DASHES = "‐‑‒–—―"


def comment_start(line):
    """Index of the comment '#' outside quotes, or -1."""
    q = None
    for i, ch in enumerate(line):
        if q:
            if ch == q:
                q = None
        elif ch in "\"'":
            q = ch
        elif ch == "#":
            return i
    return -1


def ascii_dashes(line):
    """Replace Unicode dashes with the ASCII hyphen, comment portion only."""
    i = comment_start(line)
    if i < 0:
        return line
    head, tail = line[:i], line[i:]
    for d in UNICODE_DASHES:
        tail = tail.replace(d, "-")
    return head + tail


def split_header(lines):
    """Return (pre_main_lines, rest_lines)."""
    for i, line in enumerate(lines):
        if re.match(r"^\s*main:\s*$", line):
            return lines[:i], lines[i:]
    return [], lines


def edition_for(body):
    text = "\n".join(body)
    proto = re.search(r"^\s*protocol\s*:\s*(\S+)", text, re.MULTILINE)
    proto = proto.group(1).strip().lower() if proto else ""
    if proto in ("script", "tl1", "xftp"):
        return "pro", proto
    if re.search(r"^\s*sshPrivKey\s*:", text, re.MULTILINE):
        return "pro", proto
    return "core", proto


def policy_for(rel, proto):
    if rel == BASE_TEMPLATE:
        return POLICY_BASE
    if rel in POLICY_PRO:
        return POLICY_PRO[rel]
    if proto == "tl1":
        return POLICY_TL1
    return POLICY_LEGACY


def build(rel, lines, replaces_map):
    pre, rest = split_header(lines)

    # Carry forward Status and Tested-on from an existing standard header.
    prev_status = prev_tested = None
    for line in pre:
        m = re.match(r"^##\s*Status:\s*(.*?)\s*$", line, re.IGNORECASE)
        if m:
            prev_status = m.group(1)
        m = re.match(r"^##\s*Tested-on:\s*(.*?)\s*$", line, re.IGNORECASE)
        if m:
            prev_tested = m.group(1)

    # Vendor notes: pre-main lines that are neither boilerplate nor standard
    # header fields nor the plain title line.
    notes = []
    for line in pre:
        s = line.strip()
        if not s:
            continue
        if s == TITLE or STD_FIELD_RE.match(s):
            continue
        if any(r.match(line) for r in BOILERPLATE_RE):
            continue
        notes.append(line.rstrip())

    edition, proto = edition_for(rest)
    status, tested = policy_for(rel, proto)
    if prev_status:
        status = prev_status
    if prev_tested:
        tested = prev_tested
    docs = DOCS_SCRIPT if proto == "script" else DOCS_DEFAULT

    header = [
        TITLE,
        f"## Edition: {edition}",
        f"## Status: {status}",
        f"## Tested-on: {tested}",
    ]
    old = replaces_map.get(rel)
    if old:
        header.append(f"## Replaces: {old}")
    header += [
        f"## Docs: {docs}",
        f"## Community: {COMMUNITY}",
        f"## Note: {NOTE}",
    ]

    out = [ascii_dashes(l) for l in header + notes + [""] + rest]
    return out, notes, edition, status, tested


def main():
    check = "--check" in sys.argv
    replaces_map = migration_replaces()
    changed, report = [], []

    for rel in sorted(templates()):
        path = os.path.join(REPO, rel)
        raw = open(path, "rb").read()
        had_crlf = b"\r\n" in raw
        text = raw.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
        lines = text.split("\n")
        if lines and lines[-1] == "":
            lines.pop()

        out, notes, edition, status, tested = build(rel, lines, replaces_map)
        new_text = "\n".join(out) + "\n"

        report.append((rel, edition, status, tested, notes, had_crlf))
        if new_text.encode("utf-8") != raw:
            changed.append(rel)
            if not check:
                open(path, "wb").write(new_text.encode("utf-8"))

    for rel, edition, status, tested, notes, had_crlf in report:
        flags = []
        if notes:
            flags.append(f"notes={len(notes)}")
        if had_crlf:
            flags.append("crlf->lf")
        print(f"{rel}\t{edition}\t{status}\t{tested}\t{' '.join(flags)}")

    print(f"\ntemplates: {len(report)}   changed: {len(changed)}", file=sys.stderr)
    if check and changed:
        for c in changed:
            print(f"  would change: {c}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
