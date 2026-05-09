"""Generate a small ASP fact file from the Iris dataset.

This is a lightweight preprocessing example, not the full experimental
pipeline used for all tables in the manuscript.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def atom(text: str) -> str:
    text = str(text).strip().lower()
    text = re.sub(r"[^a-z0-9_]", "_", text)
    if re.match(r"^[0-9]", text):
        text = "c_" + text
    return text


def euclidean_int(Xq: np.ndarray, Xtr: np.ndarray, scale: int) -> np.ndarray:
    diff = Xq[:, None, :] - Xtr[None, :, :]
    return np.rint(scale * np.sqrt(np.sum(diff * diff, axis=2))).astype(int)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="examples/iris_small.lp")
    parser.add_argument("--k", type=int, default=3)
    parser.add_argument("--scale", type=int, default=100)
    parser.add_argument("--test-size", type=float, default=0.2)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    data = load_iris()
    X = data.data
    y = data.target
    names = [atom(x) for x in data.target_names]

    Xtr, Xq, ytr, yq = train_test_split(
        X, y, test_size=args.test_size, stratify=y, random_state=args.seed
    )

    scaler = StandardScaler()
    Xtr = scaler.fit_transform(Xtr)
    Xq = scaler.transform(Xq)
    D = euclidean_int(Xq, Xtr, args.scale)

    lines = [f"k({args.k})."]
    for i, yi in enumerate(ytr, start=1):
        lines.append(f"train(p{i}).")
        lines.append(f"label(p{i},{names[int(yi)]}).")

    for qi, yi in enumerate(yq, start=1):
        lines.append(f"query(q{qi}).")
        lines.append(f"true_label(q{qi},{names[int(yi)]}).")
        for pi in range(1, len(ytr) + 1):
            lines.append(f"distance(q{qi},p{pi},{int(D[qi-1, pi-1])}).")

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
