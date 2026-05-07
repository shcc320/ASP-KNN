# ASP-KNN

Declarative, Constraint-Aware, and Explainable k-Nearest Neighbors in Answer Set Programming

## Overview

ASP-KNN reformulates the classical k-Nearest Neighbors (KNN) algorithm within Answer Set Programming (ASP), enabling:

- symbolic neighbor selection
- deterministic majority voting
- declarative constraint enforcement
- preference-based optimization
- interpretable reasoning traces

The framework preserves the instance-based nature of KNN while exposing the internal reasoning process through logical predicates.

This repository accompanies the paper:

> ASP-KNN: A Declarative, Constraint-Aware, and Explainable Reformulation of k-Nearest Neighbors in Answer Set Programming

## Repository Structure

```text
asp/
    ASP encodings for baseline classification, constraints,
    soft preferences, and explanation predicates.

preprocessing/
    Python scripts for distance computation and fact generation.

data/
    Example datasets used for demonstration.

examples/
    Example ASP facts and execution scripts.

docs/
    Additional documentation and reproducibility notes.
