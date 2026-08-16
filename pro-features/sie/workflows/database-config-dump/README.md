# Database config dump

Captures a MySQL or MariaDB schema as a versionable configuration artefact.

| File | What it is |
| --- | --- |
| `database-config-dump-script.yml` | The SIE template |
| `database-config-dump.sh` | The script, bash wrapping mysqldump |

## The backup-anything proof

This example is not a network device, and that is the point. If it prints to stdout and exits
with a status, rConfig can version it and diff it. An unexpected column, a dropped index or a
changed stored procedure shows up the same way a changed ACL does on a switch.

The same pattern covers plenty of other things:

| Instead of | Use |
| --- | --- |
| MySQL schema | `mysqldump --no-data --skip-dump-date --routines --triggers` |
| PostgreSQL schema | `pg_dump --schema-only` |
| Kubernetes objects | `kubectl get <resource> -o yaml` |

## Why those mysqldump flags

| Flag | Why |
| --- | --- |
| `--no-data` | Schema only. You are versioning the shape, not the contents |
| `--skip-dump-date` | Drops the timestamp comment. Without it every run differs and every diff is noise |
| `--routines` | Stored procedures and functions are part of the shape |
| `--triggers` | So are triggers |

`--skip-dump-date` is the one people miss, and it is the difference between a useful diff history
and a wall of daily false positives.

## Environment

| Variable | Required | Purpose |
| --- | --- | --- |
| `DB_HOST` | yes | Database host |
| `DB_NAME` | yes | Database to dump |
| `DB_USER` | yes | Username |
| `DB_PASSWORD` | yes | Password |
| `DB_PORT` | no | Defaults to 3306 |

The password is passed through `MYSQL_PWD` rather than on the command line, so it does not appear
in the host's process list.

## Output streams

The configuration goes to stdout and becomes the stored backup. Progress lines and the
success marker go to stderr, so the stored artefact is exactly the configuration and nothing
else. `error_patterns` and `success_patterns` are matched against stdout and stderr combined,
so putting the marker on stderr does not stop it being detected.

## Failure criteria

The template omits `exit_codes` deliberately. Omitted means any non-zero exit fails the run.
Listing an allowlist would record a crash with an unlisted code as a success, which is the
opposite of what you want from a backup job.
