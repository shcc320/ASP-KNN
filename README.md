# ASP-KNN Minimal Reproducibility Package

This repository provides a minimal reproducibility package for the manuscript:

**ASP-KNN: A Declarative, Constraint-Aware, and Explainable Reformulation of k-Nearest Neighbors in Answer Set Programming**

The package contains the ASP-KNN encoding, toy example facts, and a small preprocessing script. It is designed to support inspection and lightweight reproduction of the core reasoning mechanism, not to reproduce every experimental table in the paper.

## Repository structure

```text
asp-knn-minimal/
├── encodings/
│   ├── aspknn_core.lp       # shared ranking, neighbor selection, voting, explanations
│   ├── aspknn_v0.lp         # baseline deterministic ASP-KNN
│   ├── aspknn_forbid.lp     # exclusion-constraint extension
│   └── aspknn_soft.lp       # two-level soft preference extension
├── examples/
│   ├── toy.lp               # toy facts from the manuscript methodology section
│   ├── toy_forbid.lp        # extra forbid fact for constraint demo
│   └── soft_mode.lp         # enables soft optimization
├── scripts/
│   ├── make_iris_facts.py   # small Iris preprocessing/fact-generation example
│   └── run_example.py       # convenience runner
├── tests/
│   └── test_static_alignment.py
├── docs/
│   └── lp_alignment_note.md
└── requirements.txt
```

## Requirements

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Install an ASP solver. Either `clingo` or the `gringo` + `clasp` toolchain can be used.

## Minimal examples

Run the baseline toy example:

```bash
python scripts/run_example.py --mode v0
```

Expected final labels include:

```text
assigned_label(q1,setosa)
assigned_label(q2,versicolor)
```

Run the exclusion-constraint example:

```bash
python scripts/run_example.py --mode forbid
```

Here, `forbid(q1,setosa).` is added, so the allowed-label argmax selects the best non-forbidden label for `q1`.

Run the soft-preference example:

```bash
python scripts/run_example.py --mode soft
```

Generate a small Iris fact file:

```bash
python scripts/make_iris_facts.py --out examples/iris_small.lp --k 3 --scale 100
python scripts/run_example.py --mode v0 --facts examples/iris_small.lp
```

## Manuscript alignment

The core encoding follows the paper's pipeline:

1. generate candidate neighbors with `knn/3`;
2. rank candidates using integer-scaled distances and deterministic tie handling;
3. select top-k neighbors using `neighbor/2`;
4. aggregate label votes using `votes/3`;
5. assign labels via deterministic tie-breaking, exclusion-aware allowed-label argmax, or soft-preference optimization;
6. expose explanation atoms such as `neighbor/2`, `votes/3`, `support/3`, and `majority_evidence/3`.

See `docs/lp_alignment_note.md` for a file-by-file mapping from the manuscript to the released LP files.

## Scope and reproducibility statement

This repository contains the ASP-KNN encoding, example datasets/facts, and preprocessing scripts. It is a minimal public package intended to support reproducibility of the core method. It does not include every script used to generate all experimental tables.
