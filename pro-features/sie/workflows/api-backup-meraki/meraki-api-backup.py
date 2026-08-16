#!/usr/bin/env python3
"""Back up a Cisco Meraki organisation over the Dashboard API.

Standard library only. No CLI session is opened at any point: this is here to show that a
device with no usable CLI can still be backed up through the Script Integration Engine.

The configuration JSON goes to stdout and becomes the stored backup. Progress and the success
marker go to stderr, so the stored artefact is exactly the configuration and nothing else.
Pattern matching covers both streams, so the marker is still seen.

Environment:
    MERAKI_API_KEY    required, a Dashboard API key with read access
    MERAKI_ORG_ID     required, the organisation to back up
    MERAKI_BASE_URL   optional, defaults to the public Dashboard API

Exit codes:
    0  success
    1  any failure, with an ERROR: line on stderr
"""

import json
import os
import sys
import urllib.error
import urllib.request

BASE = os.environ.get("MERAKI_BASE_URL", "https://api.meraki.com/api/v1")
TIMEOUT = 30


def fail(message):
    print(f"ERROR: {message}", file=sys.stderr)
    sys.exit(1)


def note(message):
    print(message, file=sys.stderr)


def get(path, key):
    """GET a Dashboard API path and return the decoded body."""
    request = urllib.request.Request(
        BASE + path,
        headers={
            "X-Cisco-Meraki-API-Key": key,
            "Accept": "application/json",
            "User-Agent": "rconfig-sie-example/1.0",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        fail(f"HTTP {e.code} for {path}")
    except urllib.error.URLError as e:
        fail(f"cannot reach the Dashboard API for {path}: {e.reason}")
    except json.JSONDecodeError:
        fail(f"malformed JSON in the response for {path}")


def collect(path, key, label):
    """GET a path that is allowed to be absent on a given network."""
    try:
        return get(path, key)
    except SystemExit:
        note(f"skipped {label}, not available on this network")
        return None


def main():
    key = os.environ.get("MERAKI_API_KEY")
    org = os.environ.get("MERAKI_ORG_ID")
    if not key:
        fail("MERAKI_API_KEY is not set")
    if not org:
        fail("MERAKI_ORG_ID is not set")

    note(f"reading organisation {org}")
    networks = get(f"/organizations/{org}/networks", key)
    if not isinstance(networks, list):
        fail("the networks endpoint did not return a list")

    backup = {"organizationId": org, "networks": []}

    for network in networks:
        nid = network.get("id")
        if not nid:
            continue
        note(f"reading network {network.get('name', nid)}")
        entry = {
            "network": network,
            "devices": get(f"/networks/{nid}/devices", key),
            "vlans": collect(f"/networks/{nid}/appliance/vlans", key, "vlans"),
            "firewallL3": collect(
                f"/networks/{nid}/appliance/firewall/l3FirewallRules", key, "L3 firewall rules"
            ),
        }
        backup["networks"].append(entry)

    if not backup["networks"]:
        fail("no networks were returned, refusing to store an empty backup")

    json.dump(backup, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")

    note(f"SIE-OK: meraki backup complete, {len(backup['networks'])} network(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
