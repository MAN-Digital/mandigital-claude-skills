# Skill Optimization Protocol

Use this when the task is to review, check, optimize, update, or self-improve this skill, its registry, audit rules, Pencil workflow, or component references.

## Trigger Phrases

Run this protocol for requests like:

- "check the skill"
- "optimize the skill"
- "improve based on new skill data"
- "self improve"
- "review the skill"
- "why did another session miss this"
- "update the registry/audit based on this output"
- "it found nothing to improve"

## Required Inputs

Read these first:

1. `SKILL.md`
2. `references/master-template-fit-map.md`
3. `references/readability-depth-gate.md`
4. `references/audit-loop.md`
5. `references/qa-checklist.md`
6. `references/library-scan-loop.md`
7. Any specific reference or component file named by the user

Then search local context for fresh data:

- User memory entries about this skill, recent tests, failed nodes, corrected nodes, and exported screenshots.
- Recent artifacts under `/Users/romeoman/Documents/Codex/2026-05-26/man-digital-blog-graphics-users-romeoman/exports/` when available.
- Recent Pencil test files under `/Users/romeoman/Documents/Marketing/Design/Pencil/Skill Tests/`.
- Skill references for `Regression case`, `Hard Fail`, `TODO`, `fail`, `boring`, `mobile`, `Playground.pen`, `20 px`, `primitive`, `overlap`, `connector`, `rail`, and `random`.

## Review Procedure

1. Identify the newest user feedback or artifact that was not available when the skill was last edited.
2. Compare recent failed outputs against better outputs when both exist. For example, compare failed `b7aJDH` to the stronger `McDaW` output if those artifacts are present.
3. Determine the failure class: file hygiene, missing library scan, missing master-template scan, text scale, text overlap, heading/support collision, visual depth, connector geometry, logo asset use, random scratch nodes, format confusion, or stale repetition.
4. Check whether the current skill prevents the failure explicitly in `SKILL.md`, an audit reference, a registry reference, or a script.
5. If prevention is weak or implicit, patch the smallest durable place:
   - `SKILL.md` for startup, routing, and non-negotiable behavior.
   - `audit-loop.md` or `qa-checklist.md` for production gates.
   - `readability-depth-gate.md` for mobile/static-image failures.
   - `production-quality-floor.md` for shallow, generic, unbranded, repeated-card, or placeholder-copy failures.
   - `editable-pencil-source.md` for flattened image-only canvases or uneditable notes/text/diagram parts.
   - `hubspot-placeholder-publish.md` for uploaded exported assets, HubSpot Files API usage, placeholder replacement, and draft-only CMS patching.
   - `playground-candidate-roster.md`, `library-scan-loop.md`, and `selection-guide.md` when outputs follow brand rules but ignore high-value Playground components.
   - `library-scan-loop.md`, `component-index.md`, `master-template-fit-map.md`, or `references/components/` for component selection gaps.
   - `scripts/` only when a deterministic validation can catch the issue.
6. Validate after changes.

## No-Op Policy

Do not say "nothing to improve" just because `check_registry.py`, `check_required_nodes.py`, or `quick_validate.py` passes. Those scripts prove the folder is structurally valid; they do not prove the skill learned from new design feedback.

A no-op is allowed only when all conditions are true:

- No new user feedback, memory entry, Pencil node, screenshot, or export exists since the last skill update.
- No regression example is missing from the references or QA rules.
- `SKILL.md` startup points to the reference that handles the reported class of failure.
- A representative prompt walkthrough would run the library scan, master-template fit map when relevant, text-scale gate, zoom audit, connector audit, and file-hygiene gate.
- Validators pass.

If any condition is false, make at least one concrete update or document why the new data is already covered with exact file references.

## Regression Ledger

| Case | Failure | Required skill behavior |
| --- | --- | --- |
| `Playground.pen` edited for new graphics | New prompt content was built in the read-only library file. | Enforce one prompt-specific `.pen` per graphic and audit file hygiene. |
| Non-existent Pencil target path | A `batch_design(filePath=...)` probe against a missing `.pen` path edited the active document instead of creating the requested new file. | Before building, deleting, or replacing frames, ensure the target `.pen` exists, open it in LivePen when switching outputs, and confirm `get_editor_state` reports the intended active path. If a seed file is copied, delete/replace seed content only after confirming the active path and audit that only the intended final frame remains. |
| Unresolved Pencil write warnings | A Figma reference build produced `batch_design` `issues detected` for unsupported Lucide icon names. The full screenshot could still render enough of the design to hide the missing/inconsistent icon problem. | Treat Pencil MCP write output as a build log. Unsupported icons, invalid properties, missing assets, and render-affecting warnings are hard failures until fixed, then re-run screenshot/layout QA. |
| Figma `1091:3034` / Playground `LZkoW` reference | A separate test frame `knF6I` was created even though the same Figma-derived pattern already existed in Playground as `LZkoW`. Close-up crops for the scratch frame looked clean, but the full-frame screenshot exposed poor section fit: the outcome band initially sat too high/crowded the lower column system, then needed vertical repositioning and internal tightening. | Treat `LZkoW` in `Playground.pen` as the canonical source. Do not create new permanent reference `.pen` files when the pattern already exists in Playground. After zoom checks, run a full-frame section-fit audit. Outcome bands, footer strips, brand rails, and impact sections must sit in the vertical flow, not overlap lower cards/columns, crowd the main visual, or create a large dead gap. |
| `b7aJDH` | Key labels `OyaTH`, `u1c4n`, `SRGaY`, and `cjSnq` used 20 px Lato in a 1536 px mobile-sensitive graphic; output was primitive and ignored master nodes. | Apply static-image mobile scaling, visual-depth gate, master-template scan, and library lineage audit. |
| `NzeXF`, `TNll6`, `Aj7UL`, `uHyKq` | Heading/support text overlapped or visually merged despite whole-canvas screenshot review. | Require zoom audit, child-node inspection, and heading/support geometry checks. |
| `g2Emw` | Header/support text collided with the first visual zone because panels began at y=304 and lane labels at y=330 while the header/support stack ended at y=327. `snapshot_layout(problemsOnly)` still passed because the collision was across absolute sibling zones. | Require a structural header-to-visual-zone audit with `snapshot_layout(maxDepth: 3 or 4)` and `batch_get`: compute last header/support text bottom, compare against panel/label/card/screenshot/connector/visual-depth sibling tops, and require at least 32 px clear gap. When it fails, move the whole visual system down together, then re-export a close crop of the boundary. |
| `U5tkH`, `MJaTI`, `w94wA`, `a6Zckd`, `QqOkf`, `EB0FH`, `y36oMX`, `ERlcz`, `nsxs2` | Connectors were not smooth, aligned, or production-grade at close-up. | Apply connector port, rail, smoothness, endpoint, fill, and arrowhead gates. |
| `DyGGb`, `q64SpT`, `uVI0U`, `e9lueR` | Arrowheads looked ugly at close-up: oversized wedges, tips not audited against target gutters, loopback arrowhead direction did not match the curved route tangent, and `DyGGb` showed a curve visibly running under a pasted triangle. | Connector tips require mandatory zoom proof. Audit arrowheads as geometry: measure tip, base, connector endpoint, connector centerline, final-segment tangent, scale, and line-under-arrow overlap. For loopbacks, arrowhead direction must match the route tangent at the endpoint and the route must stop at the arrowhead base or be integrated/hidden. |
| Rail-grazing connector screenshot | A curved connector drifted into a straight vertical rail/panel edge, creating a dark seam, partial overlap, and hooked cap instead of a clean route or junction. | Audit curve-to-rail proximity at zoom. Curves must either keep a clear visible gap from rails/borders/trunks/card edges or merge through a deliberate tee/Y/integrated junction with trimmed endpoints, no doubled stroke, and no tangent collision. |
| `vfWSz` | The attempted rail fix used disconnected subpaths inside one path (`M... m...`), so the zoom export showed two broken curve fragments around the panel border. `snapshot_layout` still passed. | For user-named connectors, inspect path geometry and rendered close-up. Do not fake a gap with disconnected subpaths. Use one continuous leader, a deliberate port/notch, or separate named audited segments, then re-export the zoom crop before handoff. |
| `zRUlB` | Random/test shape appeared inside the output. | Search and remove scratch, debug, probe, temporary, and random render-test layers before handoff. |
| `nSf7c` | Alignment issue was treated as a visual nudge instead of a rail problem. | Measure parent and sibling rails; fix the alignment system, not a single by-eye offset. |
| `McDaW` | Better corrected output with stronger library DNA and mobile readability. | Treat as a positive reference when available, but do not blindly repeat its layout if another registry family fits better. |
| Container padding | Text added to pills, cards, frames, boxes, badges, callouts, or table cells lacked internal padding or margin discipline. | Use `container-spacing-and-topic-coding.md`; measure text bounds against container bounds and reject cramped components. |
| Blunt multi-topic graphics | Distinct topics such as Sales, Marketing, and Customer Success were shown with identical treatment and no fast visual differentiation. | Add restrained semantic coding: tints, lanes, chips, rails, icons, borders, grouped panels, or section headers. |
| `o204D` | A copied component cue existed as a node but disappeared visually because its fill matched the parent card background: white top accent inside a white card. | Audit cue contrast against immediate parent/background. Accent bars, top bars, chips, pills, rails, dividers, medallions, connector marks, and label surfaces must visibly contrast or be changed to an approved brand/semantic accent. |
| `ddZDg` | "Deal Stage Audit Framework" passed layout checks but was a bad design: title plus four repeated cards, no padding/gap properties, no formal components, repeated labels under every stage, no stage-specific audit logic, no logo, weak visual depth. | Use `production-quality-floor.md`; require a quality brief, library lineage, padded containers, stage-specific content or matrix structure, brand/logo treatment, and stronger visual anchor before passing. |
| Flattened image canvas | A session exported the design as an image and inserted that image into the Pencil canvas, making notes/nodes uneditable. | Use `editable-pencil-source.md`; exports are audit/publication artifacts only, while the `.pen` deliverable must keep text, notes, cards, connectors, and diagrams as editable native nodes. |
| `ZBw56` | A full-height Medium Blue left brand plane consumed about 15% of a 1536 x 1024 blog graphic while carrying only a small logo. It reduced the main visual area and added brand color without meaning. | Add the composition-efficiency gate: no large logo-only brand slabs, empty sidebars, or dead color planes. Large planes must carry content, define a meaningful lane, frame the main visual, or be removed/reduced. |
| `bczuO`, `zshts` | Visible `Article context: ...` / rationale copy was added inside a blog graphic even though the finished graphic replaces the placeholder inside the article and the article page already provides that context. | Treat article context as private planning input only. Ban visible article-context, prompt/context paths, placeholder labels, prompt-rationale, section-rationale, `Reason X...`, or internal audit/planning notes. Only add a source/caption when the user explicitly asks or a real external citation is required. |
| HubSpot placeholder queue | A fetched blog post can contain several `div.man-graphic-placeholder` blocks with prompts after `Prompt to use in Figma:`; missing blocks or making one generic graphic loses required blog visuals. | Use `hubspot-post-fetch.md`; fetch the dynamic post target, read `*.graphic-placeholders.json`, create one separate editable `.pen` per extracted prompt, and treat placeholder `References:` links as context only. |
| HubSpot prompt without article context | A placeholder prompt may be extracted correctly but still lose the article's terminology, argument, audience, and sequence if designed in isolation. | The fetcher must write `*.article-context.md`; every prompt file and production queue item must point to it, and the skill must require reading it before planning, component selection, editing, and audit. |
| HubSpot output placement naming | The generated `.pen` files and top-level frames kept slug/test names, so the user could not reliably match finished graphics back to the blog placeholder order. | For every fetched HubSpot placeholder output, name both the `.pen` file and final top-level frame `{Blog Title} - {Blog Post ID} - Graphic {Number} - {Graphic Title Name}` using the original top-to-bottom placeholder number. Preserve skipped numbers when only a subset exists. |
| HubSpot Files/CMS placement | Finished graphics need to be uploaded to HubSpot Files and inserted into the matching `div.man-graphic-placeholder` blocks. Doing this ad hoc risks patching live content, losing `postBody`, mismatching images to placeholders, or publishing prompt text. | Use `hubspot-placeholder-publish.md` and `scripts/hubspot_placeholder_publish.py`: export audited frames, upload to the user-specified folder, replace placeholders in manifest order, write original/patched backups, and PATCH only the draft endpoint after explicit confirmation. |
| HubSpot image optimization | Uploads can accidentally use PNG exports, generic node-ID filenames, or omit alt/title markup. HubSpot Files API upload options control access/indexing, not rendered blog-image alt text. | For placement runs, export/prepare 1x WebP assets with quality 100/lossless by default, use SEO-friendly title-derived `fileName`, add descriptive `alt` and `title` attributes to replacement `<img>` markup, and record prepared WebP paths in the upload manifest. |
| HubSpot publication without traceable `.pen` files | A HubSpot placement test used deterministic publication WebPs after Pencil screenshot/export returned blank child layers, so the draft received images without one prompt-specific editable `.pen` source per graphic. This made the assets hard to trace and violated the user's source expectations. | Treat blank/stale Pencil export as a blocker. For upload/patch runs, require `source_pen_path` for every asset, one unique `.pen` per graphic, no `Playground.pen`, preserved graphic number in the filename, and matching article-placement naming. Only use `--allow-missing-pen-source` after explicit user approval and disclose the limitation. |
| Misaligned status pill text | A published HubSpot graphic had a `Draft mode` pill whose text sat low/was not centered inside the rounded cyan fill. Full-canvas/mobile preview did not catch it strongly enough. | Add a pill/chip/badge alignment gate: measure label centerline against container centerline, confirm top/bottom padding, and inspect a close-up crop of the most crowded pill plus a representative repeated pill before upload or handoff. |
| `cV3XM` | A one-word process/card label (`Measurement`) wrapped/broke into an unintended second line because the label zone was too narrow or the text mode allowed wrapping. | Treat one-word and short step/card labels as one-line by default. Reserve enough width/height, use one-line text mode where appropriate, and close-up audit the representative longest label before export. |
| Graphic 4 `dashboard` wording | A conceptual measurement scorecard was titled as a dashboard, creating a false expectation of an actual HubSpot dashboard or screenshot. | Audit visible artifact nouns. Use `dashboard` only when the graphic depicts a dashboard UI; otherwise use `scorecard`, `report`, `model`, `framework`, or `measurement view`. |
| Export-only bar/text overlap | A scorecard export showed mini bars/progress elements stacked over labels/body text even though earlier full-frame screenshot review did not catch the issue strongly enough. | Inspect the final exported WebP/PNG itself before upload or handoff. Reject exports where chart bars, progress fills, labels, or cards overlap text; rebuild the native Pencil source and re-export. |
| `l9vKx` | Graphic 1 passed `snapshot_layout(problemsOnly)` but still looked bad for a HubSpot blog graphic: tiny process cards, tiny handoff labels, shallow visual hierarchy, weak process-map anatomy, and no serious pre-upload critique. | HubSpot upload requires a human-grade pre-publication visual audit. Inspect the full frame, close-up of the densest/risky child region, and final exported WebP/PNG. Reject primitive, cramped, tiny, or under-designed graphics before upload even when structural layout passes. |
| Registry present but not used | The skill had component refs for strong Playground nodes such as `fKn3K`, `pAw6X`, `sQ8TR`, `LZkoW`, `EdtGZ`, `v5aVuG`, `lLDFt`, `SbBJV`, `G7EWZ`, `G6YkCq`, `nia9w`, `DJN2N`, `jNmrp`, `NhErk`, `Y3Tzyc`, `zuu8y`, `lP11x`, `HoOjV`, `l5NNCU`, `s2ZqRB`, `KVqAt`, `tMsEe`, `b8SoH`, `llyux`, `PPpdM`, `nRPmP`, and `S20AXj`, but the workflow only hard-forced five master nodes plus generic "compare three candidates." Agents could satisfy brand/design-system checks without using these mature components. | Require `playground-candidate-roster.md`: before building, name exact node IDs for primary, alternate, and supporting candidates; inspect the primary live with Pencil `batch_get`; fail brand-system-only builds with no Playground lineage; update `template-coverage.md` so required-node validation includes the high-value roster. |

## Output Expectations

When responding to a skill-optimization request:

1. State which files changed, or provide the no-op evidence.
2. State which new feedback/regression was encoded.
3. State validation commands and results.
4. State remaining risks or follow-up needs.

Keep the response concise. The user needs to know whether the skill actually changed and whether the change is installed and synced.
