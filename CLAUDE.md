# CLAUDE.md

## What this repo is

Community connection templates for rConfig V8 Core and Pro.

## Working rules for any Claude session in this repo

- Work is governed by Stephen's action plan. No work outside an approved item.
- Never commit or push without Stephen's explicit go for the specific change.
- Deviations: stop, describe the deviation simply, wait for approval.
- `restructure/v2` is read-only reference. Never merge or cherry-pick from it.
- Report changes as concise diff summaries.

## Code and content standards

This is a living section. It is seeded now and extended as standards are adopted.

- Markdown and YAML comments never use the em dash character.
- All free-text YAML values are wrapped in double quotes.
- Filenames and directories are lowercase and hyphenated. The full naming convention will be recorded here when adopted in Phase 2.
- Vendor directories are named for the lowercase common short form of the vendor name. Examples: `palo-alto`, `edgecore`, `checkpoint`, `digi`, `rad`.
- Directories prefixed with an underscore are reserved for non-vendor content that must sort above the vendor listing. `_base` holds the starter template.
- Commit messages use the plan item prefix `P<phase>.<item>`, for example `P1.1`.
- Every adopted standard MUST be added to this file in the same change that adopts it.

## Verification

Run `scripts/validate_templates.py` before reporting any template change complete.

Note: this script arrives in a later phase. This line is a forward reference.
