# LP alignment note

This repository is intentionally a reproducibility materials package rather than a complete archive of every experiment.

## Manuscript-to-code mapping

| Manuscript component | Repository file | Status |
|---|---|---|
| Candidate relation `knn/3` | `encodings/aspknn_core.lp` | Included |
| Stable distance ranking `rank/3` using `lt/3` and `eqd/3` | `encodings/aspknn_core.lp` | Included |
| Top-k neighbor selection `neighbor/2` | `encodings/aspknn_core.lp` | Included |
| Vote aggregation `votes/3` | `encodings/aspknn_core.lp` | Included |
| Baseline deterministic lexicographic tie-breaking | `encodings/aspknn_v0.lp` | Included |
| Label exclusion over allowed labels | `encodings/aspknn_forbid.lp` | Included |
| Two-level soft preference using mismatch count and farthest supporter distance | `encodings/aspknn_soft.lp` | Included |
| Explanation atoms `support/3` and `majority_evidence/3` | `encodings/aspknn_core.lp` | Included |

## Important adjustment from earlier draft code

The earlier `aspknn_soft.lp` draft used a distance-weighted mismatch objective. The manuscript text describes a different lower-priority objective: minimizing the farthest supporting-neighbor distance of the predicted label. The released `encodings/aspknn_soft.lp` therefore implements the manuscript version using `support_dist/3` and `max_support_dist/3`.

## Scope

The repository provides:

- ASP encodings for the baseline, exclusion, and soft-preference variants;
- a toy example matching the methodology section;
- a small Iris fact-generation script showing preprocessing and integer distance scaling;
- a simple runner script.

