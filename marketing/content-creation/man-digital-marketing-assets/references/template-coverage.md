# Template Coverage

This skill must consider the whole Playground and carousel-derived template library, not only the nodes recently requested by the user. The lists below are required top-level routing nodes. Some already have deep anatomy docs; others are route-level references that must be inspected with Pencil before use.

## Cover Families

| Node IDs | Use for |
| --- | --- |
| `P1lJ4`, `nXTXW`, `m0AGw`, `bjCb3`, `rCfDQ`, `xJySU`, `EuJZZ`, `81xtN`, `sLZgV`, `9Nac9`, `z8Ai1`, `toIXr`, `XYYB5`, `dI0RZ`, `qIQkx`, `GK1cz`, `nAN4b`, `Oaaf3`, `nDCxe`, `MDZoE`, `V55uo`, `El1Np`, `1GRXD`, `x73R0`, `loMOa` | Carousel covers, section labels, 1:1/4:5/16:9 cover variants, CTA/closing frames, blog hero/OG covers. |

## Slide And Carousel Template Families

| Pattern | Node IDs |
| --- | --- |
| Slide 2 / early argument templates | `Wf0kc`, `5MGHD`, `M9Mwq`, `lk5IY`, `AGj6s`, `VqQ1q`, `MEygm`, `XU9Jh`, `pNnmc`, `nYhge`, `xzcQj`, `Vmhgt`, `V5iH8`, `chxsV`, `rOwJz`, `Uyaly`, `IfWXj`, `s2Djt`, `KTCK6`, `DSNAg`, `4XjgY`, `ANwLg`, `mGR6X`, `S83Yn`, `xrbbT`, `Ss4XV`, `PCERa`, `Wn3fM`, `OxE0i`, `pArwu`, `sW4Qc`, `69qqe`, `enyqD`, `Gagt6` |
| Slide 4 / decision and sequence templates | `FCw4P`, `dSYM9`, `sLRvD`, `kpDtk`, `9QojL`, `ul9DN`, `5kXd2`, `uGUnu`, `9ucOy`, `WsUV2`, `DIdDa`, `VoeXd`, `IqpRv`, `lLFX3`, `UE3nt` |
| Slide 5 / impact and framework templates | `dNJMv`, `eYM78`, `XBFUT`, `Pd0Ar`, `tqRKw`, `1wobI` |
| Slide 6 / lifecycle and process templates | `5hcRD`, `jWyvs`, `cvoYg`, `fVYda`, `ONaC7`, `u7BvG` |
| Slide 7 / scorecard, warnings, takeaways, tables | `GRV8P`, `gASqb`, `ffT7v`, `LGDxt`, `DW3dd`, `RXIfB`, `1LmMQ` |
| 16:9 slide support pieces and variants | `YO7kf`, `TEAdJ`, `v2O4y`, `ZczXl`, `kzjzN`, `FmG17`, `oAlzD`, `UGkI1`, `zLUkh`, `GUuGw`, `gOlaQ`, `FXb6g`, `Fe8ZR`, `r4XvN`, `kRJNr` |

## Required Discipline

## High-Value Blog And Prospecting Families

These are not optional examples. They are required top-level routing nodes for MAN Digital blog and HubSpot/RevOps/prospecting graphics, and `scripts/check_required_nodes.py` must keep component refs for them.

| Family | Node IDs |
| --- | --- |
| Signal-to-revenue / HubSpot system explainers | `nRPmP`, `KVqAt`, `tMsEe`, `b8SoH`, `llyux` |
| Prospecting Agent vs Outbound vertical explainers | `S20AXj`, `l5NNCU`, `EdtGZ`, `LZkoW`, `sQ8TR`, `pAw6X`, `fKn3K` |
| Prospecting-Agent 1080x1350 sequence | `PPpdM`, `s2ZqRB`, `v5aVuG`, `lLDFt`, `SbBJV`, `G7EWZ`, `G6YkCq`, `nia9w`, `DJN2N`, `jNmrp`, `NhErk`, `Y3Tzyc`, `zuu8y`, `lP11x`, `HoOjV` |

## Required Discipline

1. Before using any listed node, load its `references/components/<node-id>.md` file and inspect the live Pencil node with `batch_get`.
2. Before creating a MAN Digital blog, HubSpot, RevOps, prospecting, outbound, signal, AI, workflow, or article graphic, run `playground-candidate-roster.md` and name exact node IDs for primary, alternate, and supporting candidates.
3. If the reference is route-level only, take a screenshot and inspect child nodes before editing.
4. For repeated future use, upgrade route-level refs into full anatomy docs.
5. Use `scripts/check_required_nodes.py` after adding or changing this list.
