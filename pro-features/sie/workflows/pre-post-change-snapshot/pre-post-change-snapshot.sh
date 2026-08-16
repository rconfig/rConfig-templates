#!/usr/bin/env bash
#
# Capture a delimited operational state snapshot from a device over SSH.
#
# Run it before a change window and again after. rConfig stores each run as a version, so the
# diff between the two is the evidence of what the change actually did.
#
# The snapshot goes to stdout and becomes the stored backup. Progress and the success marker go
# to stderr, so the stored artefact is exactly the device output and nothing else. Pattern
# matching covers both streams, so the marker is still seen.
#
# Environment:
#     SNAPSHOT_HOST    required, device hostname or IP
#     SNAPSHOT_USER    required, SSH username
#     SNAPSHOT_PORT    optional, defaults to 22
#
# Authentication is by SSH key. BatchMode is on, so the script fails rather than hanging on a
# password prompt. Put the key on the rConfig host for the account that runs the job.
#
# Exit codes:
#     0  success
#     1  any failure, with an ERROR: line on stderr

set -o pipefail

HOST="${SNAPSHOT_HOST:-}"
USER_NAME="${SNAPSHOT_USER:-}"
PORT="${SNAPSHOT_PORT:-22}"

fail() {
    echo "ERROR: $1" >&2
    exit 1
}

[ -n "$HOST" ] || fail "SNAPSHOT_HOST is not set"
[ -n "$USER_NAME" ] || fail "SNAPSHOT_USER is not set"

COMMANDS=(
    "show running-config"
    "show ip interface brief"
    "show ip route summary"
    "show cdp neighbors detail"
    "show version"
)

echo "connecting to $HOST as $USER_NAME" >&2

for command in "${COMMANDS[@]}"; do
    # A fixed delimiter per section keeps the diff readable. Without it, a single line moving
    # between sections looks like two unrelated changes.
    echo "===== ${command} ====="

    if ! ssh -o BatchMode=yes \
             -o StrictHostKeyChecking=accept-new \
             -o ConnectTimeout=10 \
             -p "$PORT" \
             "${USER_NAME}@${HOST}" \
             "$command"; then
        fail "command failed on ${HOST}: ${command}"
    fi

    echo
done

echo "===== end of snapshot ====="

echo "SIE-OK: snapshot complete, ${#COMMANDS[@]} section(s) from ${HOST}" >&2
exit 0
