# rConfig-templates: Phased Action Plan and Tracker

Companion to GOALS.md. One item per line of work, top to bottom, plain language. Nothing happens that is not an item here, and no item runs without Stephen's APPROVED mark.

Status: POPULATED from the restructure/v2 survey, all items PROPOSED, awaiting Stephen's top-to-bottom pass
Last updated: 7 August 2026

---

## Rules of engagement

1. Every item aligns to a goal (G1 to G5) or sits under a Non-Aligned heading. No third category.
2. Each item must be understandable from its one-line text. If it cannot be said simply, it gets split.
3. Lifecycle: PROPOSED, APPROVED (Stephen), IN PROGRESS, DONE, VERIFIED (Stephen). REJECTED or DEFERRED at any point. Items marked DECISION need an answer, not work.
4. No commits without approval. Work is applied, diff summarized, committed only on Stephen's go.
5. Deviations stop work and come back as a new PROPOSED item before anything proceeds.
6. Implementation discoveries go to the Findings Log, never straight into action.

## Ground rules for THIS effort (Stephen, fixed)

- The default branch is renamed to main first. A BRAND NEW branch is created from main. All work is fresh commits on that new branch.
- restructure/v2 is READ-ONLY REFERENCE MATERIAL. Nothing is merged or cherry-picked from it as commits; where we adopt its work we re-apply it cleanly (rerun its scripts or re-create the files) so every change passes through this plan.
- restructure/v2 is DELETED (local and remote) at the end.
- Source column meanings: PORT = re-apply from v2 essentially as-is; REWORK = adopt from v2 with stated changes; NEW = fresh; DECISION = needs Stephen's answer first.

## Explicitly NOT carried from restructure/v2

Starting fresh from main means these simply never happen unless promoted into an item:

1. The telnet saveConfig blankings (all 10 templates keep their original save commands, including base.yml "wr mem").
2. The ctrlYLogin and auth.linebreak key removals (both keys stay in their templates).
3. The parser-forensics layer: the 88 file:line citations, ORDER-OF-OPERATIONS section 2 protocol traces, TEMPLATES.md section 9, the v8-parser-verification-prompt.md file, and all 13 inline "issue N" product-bug references.
4. The ftp inbound and protocol-fallback starter templates (they exist only because of the parser pass).
5. The Tested-on rewrite asserting V8 coverage on 60 templates (returns as a DECISION item, P3.9).

---

## Phase 0: Repo admin (Non-Aligned)

| ID | What | Goal | Source | Status |
|---|---|---|---|---|
| P0.1 | Rename the default branch master to main on GitHub (auto-redirects old links), update local clones | Non-Aligned | NEW | PROPOSED |
| P0.2 | Confirm credential hygiene is complete: old PAT revoked, no token in any remote URL, gh supplies credentials | Non-Aligned | NEW | PROPOSED |
| P0.3 | Create the new working branch from main (name to agree, e.g. v2-rebuild); restructure/v2 becomes read-only reference from this moment | Non-Aligned | NEW | PROPOSED |
| P0.4 | Hygiene on the new branch: delete the leftover AI-chat line at the end of README.md, untrack .vscode/settings.json, gitignore .vscode/ .idea/ .DS_Store .todo __pycache__/ | Non-Aligned | PORT | PROPOSED |

## Phase 1: Structure (G2)

| ID | What | Goal | Source | Status |
|---|---|---|---|---|
| P1.1 | Rename all 27 mixed-case vendor directories to lowercase hyphenated (two-step moves for case-only renames), e.g. Palo_Alto_Networks to palo-alto | G2 | PORT | PROPOSED |
| P1.2 | Move base/ to _base/ so the starter template sorts to the top | G2 | PORT | PROPOSED |
| P1.3 | Merge Mellanox/ into nvidia/ (Mellanox is NVIDIA Networking) | G2 | PORT | PROPOSED |
| P1.4 | Move the misfiled Aruba/HP-A5120 template into hp/ (it is Comware, not Aruba) | G2 | PORT | PROPOSED |
| P1.5 | Move README-NONINTERACTIVEMODE-SSH.md to docs/noninteractive-ssh.md and huawei/hua-ssh-noenable.md to huawei/README.md | G2 | PORT | PROPOSED |
| P1.6 | Create docs/MIGRATION.md: the complete old-path to new-path map for every rename and deletion, so the clean cut is navigable | G2 | PORT | PROPOSED |
| P1.7 | Fix vendor README references broken by the renames (cisco, huawei, mikrotik, fortinet, palo-alto, pfsense pointed at old filenames and v6-era wording) | G2 | PORT | PROPOSED |

## Phase 2: Naming (G3)

| ID | What | Goal | Source | Status |
|---|---|---|---|---|
| P2.1 | Adopt the naming convention vendor-osfamily[-version]-protocol-authmode[-variant].yml, documented with a token table and the rule that hardware models appear only when the model changes connection behavior | G3 | PORT | PROPOSED |
| P2.2 | Bulk-rename all existing templates onto the convention (67 renames, git mv so history survives) | G3 | PORT | PROPOSED |
| P2.3 | Dell collapse: s4048 becomes dell-networking-ssh-noenable (universal), 5524/6248 become the two dell-powerconnect-telnet variants | G3 | PORT | PROPOSED |
| P2.4 | PAN-OS keeps its version split: panos-9x stays a distinct template alongside the current one (the vendor with real version nuance) | G3 | PORT | PROPOSED |
| P2.5 | Models kept where behavior demands it: hp-1920 (needs _cmdline-mode), hp-5400xl, ciena-6500 (TL1) | G3 | PORT | PROPOSED |
| P2.6 | Name-vs-content corrections: ruckus "Enable" file is actually enable off, ubiquiti "no-enable" is actually enable on, hp-5400xl was mislabeled; filenames follow the content | G3 | PORT | PROPOSED |
| P2.7 | ProCurve paging variants: keep BOTH the deliberate "nno page" template and the plain "no page" variant, with the hp/README.md explanation of the swallowed-first-character quirk | G3 | PORT | PROPOSED |
| P2.8 | Delete the two superseded v1 templates (mikrotik v1, panos v1), recorded in MIGRATION.md | G3 | PORT | PROPOSED |
| P2.9 | Correct the ~14 wrong display names (main.name/desc): "MikroTek SSH nnoenable", "JUNOS_SWITCHES", stale "v2 for v6 users" wording, the 5400xl copy-paste error | G3 | PORT | PROPOSED |
| P2.10 | linux/centos-7 becomes linux-el (covers RHEL/CentOS/Rocky/Alma) | G3 | PORT | PROPOSED |

## Phase 3: The Legend (G4)

| ID | What | Goal | Source | Status |
|---|---|---|---|---|
| P3.1 | DECISION, gates this whole phase: the legend's depth. Option A: document keys from observed use and vendor knowledge, no parser claims at all. Option B: keep the corrected behavioral facts from v2 (e.g. the on/off vs true/false trap, per-protocol notes) but stated plainly, with zero file:line citations and zero product-bug references. Option C: keep the full forensic layer (rejected by the fence in GOALS.md unless promoted) | G4 | DECISION | PROPOSED |
| P3.2 | Standard 7-line header on every template (Edition, Status, Tested-on, Replaces, Docs, Community, Note), applied by a repeatable script, vendor notes preserved | G4 | PORT | PROPOSED |
| P3.3 | Remove the two deprecated keys (pagerPrompt, pagerPromptCmd) from all templates; safe because master's own comments already mark them deprecated | G4 | PORT | PROPOSED |
| P3.4 | docs/TEMPLATES.md, the legend: anatomy of a template, the "connection here, retrieval commands in rConfig Command Groups" rule, the OOO summary, and the per-section key tables (depth of the Notes column per P3.1) | G4 | REWORK | PROPOSED |
| P3.5 | docs/ORDER-OF-OPERATIONS.md: the seven-stage principle ("a template is a script of what rConfig does, in order, not a bag of settings"), stage-to-key map, the annotated Cisco session, the three contrasting vendor shapes, and the debug-by-stage guide (cleaned per P3.1) | G4 | REWORK | PROPOSED |
| P3.6 | The new-key request process: docs section plus the GitHub issue form that requires the OOO stage, why existing keys cannot express the behavior, and a sanitized transcript | G4 | PORT | PROPOSED |
| P3.7 | scripts/validate_templates.py plus the CI workflow: header, key names against the legend, deprecated keys, name uniqueness, filename convention | G4 | PORT | PROPOSED |
| P3.8 | docs/CONTRIBUTING.md: convention, header spec, status meanings, content rules, submission steps | G4 | REWORK | PROPOSED |
| P3.9 | DECISION: the Tested-on wording for the 60 existing templates. Option A: hedged, "rConfig V6/V7 era, retest on V8 welcome". Option B: assert "rConfig V6, V7 and V8" as vendor policy. (v2 chose B late; starting value is whatever you pick here) | G4 | DECISION | PROPOSED |

## Phase 4: Vendor expansion (G1)

| ID | What | Goal | Source | Status |
|---|---|---|---|---|
| P4.1 | Add the 12 vendor starter templates across 10 new vendor dirs: arista (x2), f5, a10, nokia (x2), alcatel-lucent, zte, zyxel, netgear, tp-link, opengear, all marked untested-starter, vendor quirks noted in-file | G1 | PORT | PROPOSED |
| P4.2 | Short README per new vendor dir: device families, typical retrieval commands to attach in rConfig, test-report call to action | G1 | PORT | PROPOSED |
| P4.3 | The template-test-report issue form, the promotion path from untested-starter to community-tested | G1 | PORT | PROPOSED |
| P4.4 | Rewrite the root README: quick start, docs index, status legend with the test-report link, honest vendor-count badge | G1 | REWORK | PROPOSED |
| P4.5 | Resolve the opengear starter's guessed values (it was modeled on the Linux template and marked VERIFY in v2): confirm or adjust before it ships | G1 | REWORK | PROPOSED |

## Phase 5: Pro features (G5)

| ID | What | Goal | Source | Status |
|---|---|---|---|---|
| P5.1 | Consolidate SIE-Base, SIE-Radware, SIE-Zyxel and SSH-Private-Key under one pro-features/ tree | G5 | PORT | PROPOSED |
| P5.2 | docs/EDITIONS.md: the core vs pro capability matrix, framed as what is supported per edition, with TL1 marked pro (it lives in ciena/) | G5 | REWORK | PROPOSED |
| P5.3 | Rewrite the SIE, radware, zyxel and ssh-private-key READMEs for V8 (drop the "V7 Pro, may come to core" era wording) | G5 | PORT | PROPOSED |
| P5.4 | The four SIE workflow examples (meraki REST backup, pre/post change snapshot, multi-step firewall export, database schema dump), each a README plus template plus script; database-config-dump doubles as the "back up anything" proof | G5 | PORT | PROPOSED |
| P5.5 | pro-features/xftp/: README explaining the inbound file service and the fact that there is no xFTP connection template, plus push-commands.md with starter device-side push commands | G5 | REWORK | PROPOSED |
| P5.6 | Mark edition in every template header (core = works on both, pro = Pro only) so the repo stops implying everything works everywhere | G5 | PORT | PROPOSED |

## Phase 6: Publish and close out (Non-Aligned)

| ID | What | Goal | Source | Status |
|---|---|---|---|---|
| P6.1 | Push the new branch, confirm CI green on GitHub | Non-Aligned | NEW | PROPOSED |
| P6.2 | Open the PR to main: renames with the MIGRATION map, the two deletions, the starter count, no behavior changes to any template | Non-Aligned | NEW | PROPOSED |
| P6.3 | Merge (no squash, keep rename history usable), post-merge spot checks | Non-Aligned | NEW | PROPOSED |
| P6.4 | DELETE restructure/v2, local and remote, per the ground rule | Non-Aligned | NEW | PROPOSED |
| P6.5 | Optional: pinned "starters seeking test reports" issue as the community campaign | Non-Aligned | NEW | PROPOSED |
| P6.6 | Optional: adopt the MikroTik +cte guidance correction (small, correct, but maps to no goal; approve or drop) | Non-Aligned | REWORK | PROPOSED |

---

## Findings Log

- 2026-08-07: survey confirms restructure/v2 working tree is clean and all walk fixes (W1/W2) were committed on that branch; since v2 is now reference-only, they need no disposition, they simply inform P3.9 and item wording.
- (new findings land here)

## Change log

- 2026-08-07: skeleton created.
- 2026-08-07: populated from the restructure/v2 survey. Ground rules fixed per Stephen: main rename first, brand-new branch from main, v2 reference-only and deleted at the end. Not-carried list written from the survey's overreach section.
