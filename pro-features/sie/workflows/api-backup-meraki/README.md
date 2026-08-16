# API backup: Cisco Meraki

Backs up a Meraki organisation over the Dashboard API. **No CLI session is opened at any point.**

| File | What it is |
| --- | --- |
| `meraki-api-backup-script.yml` | The SIE template |
| `meraki-api-backup.py` | The script, python3 standard library only |

## What it does

Reads the organisation's networks, then for each network collects the device list, the appliance
VLANs and the L3 firewall rules. The combined result is printed as sorted, indented JSON, which
is what rConfig stores. Sorting the keys matters: without it the API's ordering can change between
runs and every backup looks like a diff.

Endpoints that do not apply to a given network, such as VLANs on a network with no appliance, are
skipped with a note rather than failing the run.

## Why this example exists

Plenty of hardware has no usable CLI. This shows that such a device is still backupable: the
Script Integration Engine does not care whether the script talks SSH, HTTP or anything else, only
what it prints and what it exits with.

## Environment

| Variable | Required | Purpose |
| --- | --- | --- |
| `MERAKI_API_KEY` | yes | Dashboard API key with read access |
| `MERAKI_ORG_ID` | yes | Organisation to back up |
| `MERAKI_BASE_URL` | no | Defaults to the public Dashboard API |

## Output streams

The configuration goes to stdout and becomes the stored backup. Progress lines and the
success marker go to stderr, so the stored artefact is exactly the configuration and nothing
else. `error_patterns` and `success_patterns` are matched against stdout and stderr combined,
so putting the marker on stderr does not stop it being detected.

## Failure criteria

The template omits `exit_codes` deliberately. Omitted means any non-zero exit fails the run.
Listing an allowlist would record a crash with an unlisted code as a success, which is the
opposite of what you want from a backup job.
