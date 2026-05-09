# ASP-KNN Reproducibility Package

This repository provides reproducibility materials for the manuscript:

**ASP-KNN: A Declarative, Constraint-Aware, and Explainable Reformulation of k-Nearest Neighbors in Answer Set Programming**

It contains the ASP-KNN encodings, example ASP fact files, and preprocessing scripts corresponding to the method described in the manuscript. The repository is intended to make the released encoding and example pipeline inspectable and runnable. It is not a full archival dump of every experimental script used to produce all tables in the paper.

## Repository structure

```text
asp-knn-reproducibility/
├── encodings/
│   ├── aspknn_core.lp       # shared ranking, neighbor selection, voting, explanations
│   ├── aspknn_v0.lp         # baseline deterministic ASP-KNN
│   ├── aspknn_forbid.lp     # exclusion-constraint extension
│   └── aspknn_soft.lp       # two-level soft preference extension
├── examples/
│   ├── toy.lp               # toy facts matching the methodology example
│   ├── toy_forbid.lp        # forbid fact for the exclusion demo
│   └── soft_mode.lp         # enables soft optimization
├── scripts/
│   ├── make_iris_facts.py   # Iris preprocessing/fact-generation example
│   └── run_example.py       # command-line runner for examples
├── tests/
│   └── test_static_alignment.py  # optional static consistency checks
├── docs/
│   └── lp_alignment_note.md # mapping from manuscript descriptions to LP files
└── requirements.txt
```

## Requirements

### Python dependencies

```bash
python -m pip install -r requirements.txt
```

### ASP command-line solver

The examples require a Potassco ASP command-line solver, not only a Python package.

Recommended option:

```bash
clingo --version
```

The manuscript runtime section used the Potassco toolchain with `gringo 5.7.1` and `clasp 3.3.10`. In practice, the repository runner supports either:

1. `clingo`, the combined grounder-and-solver executable; or
2. separate `gringo` + `clasp` command-line executables.

Download/install references:

- Potassco clingo page: https://potassco.org/clingo/
- Potassco getting started page: https://potassco.org/doc/start/
- clingo releases: https://github.com/potassco/clingo/releases
- clasp releases: https://github.com/potassco/clasp/releases
- Potassco guide: https://github.com/potassco/guide

Typical installation commands depend on the operating system:

```bash
# macOS with Homebrew
brew install clingo

# Ubuntu/Debian; package naming may expose gringo/clasp separately
sudo apt-get update
sudo apt-get install clingo

# Conda, often convenient on Windows/Linux/macOS
conda install -c conda-forge clingo
```

After installation, verify one of the following:

```bash
clingo --version
```

or

```bash
gringo --version
clasp --version
```

## Running examples

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

Generate a small Iris fact file and classify it:

```bash
python scripts/make_iris_facts.py --out examples/iris_small.lp --k 3 --scale 100
python scripts/run_example.py --mode v0 --facts examples/iris_small.lp
```

## Optional static alignment test

`tests/test_static_alignment.py` is not a manuscript experiment and does not replace solver-based reproduction. It is an optional repository-maintenance check that verifies the released LP files still contain the key rules described in the paper: stable ranking, top-k neighbor selection, vote aggregation, lexicographic tie-breaking, exclusion-aware allowed-label argmax, and two-level soft preference optimization.

Install pytest if needed:

```bash
python -m pip install pytest
```

Run the static test:

```bash
python -m pytest tests/test_static_alignment.py
```

This test does not require `clingo`, `gringo`, or `clasp`; it only checks the text of the LP files. Passing this test means the repository has not accidentally removed or renamed core rules. It does not prove that all experimental results in the manuscript are reproduced.

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

This public repository contains the ASP-KNN encoding, example datasets/facts, and preprocessing scripts corresponding to the reproducibility statement in the manuscript:

> To support reproducibility, the ASP-KNN encoding, example datasets, and preprocessing scripts used in this study are available from the corresponding author upon reasonable request. A public repository containing these materials will be provided upon acceptance of the manuscript.

The repository name therefore avoids the word `minimal` in the public-facing title. The scope is described as a reproducibility-materials repository rather than a complete experiment-reproduction archive.
