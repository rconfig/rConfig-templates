#!/usr/bin/env bash
#
# Capture a MySQL or MariaDB schema as a versionable configuration artefact.
#
# Schema only, no row data. The point is to version the shape of the database the way you version
# a switch configuration, so an unexpected column or a dropped index shows up in a diff.
#
# The dump goes to stdout and becomes the stored backup. Progress and the success marker go to
# stderr, so the stored artefact is exactly the SQL. Pattern matching covers both streams, so the
# marker is still seen.
#
# Environment:
#     DB_HOST        required, database host
#     DB_NAME        required, database to dump
#     DB_USER        required, username
#     DB_PASSWORD    required, password
#     DB_PORT        optional, defaults to 3306
#
# Exit codes:
#     0  success
#     1  any failure, with an ERROR: line on stderr

set -o pipefail

HOST="${DB_HOST:-}"
NAME="${DB_NAME:-}"
USER_NAME="${DB_USER:-}"
PASSWORD="${DB_PASSWORD:-}"
PORT="${DB_PORT:-3306}"

fail() {
    echo "ERROR: $1" >&2
    exit 1
}

[ -n "$HOST" ]      || fail "DB_HOST is not set"
[ -n "$NAME" ]      || fail "DB_NAME is not set"
[ -n "$USER_NAME" ] || fail "DB_USER is not set"
[ -n "$PASSWORD" ]  || fail "DB_PASSWORD is not set"

command -v mysqldump >/dev/null 2>&1 || fail "mysqldump is not on PATH"

echo "dumping schema for ${NAME} on ${HOST}" >&2

# --no-data        schema only, no rows
# --skip-dump-date drops the timestamp comment, otherwise every run is a spurious diff
# --routines       include stored procedures and functions
# --triggers       include triggers
#
# The password is passed through the environment rather than on the command line, so it does not
# appear in the host's process list.
if ! MYSQL_PWD="$PASSWORD" mysqldump \
        --host="$HOST" \
        --port="$PORT" \
        --user="$USER_NAME" \
        --no-data \
        --skip-dump-date \
        --routines \
        --triggers \
        "$NAME"; then
    fail "mysqldump failed for ${NAME} on ${HOST}"
fi

echo "SIE-OK: schema dump complete for ${NAME}" >&2
exit 0
