"""Run a minimal ASP-KNN example using clingo or gringo+clasp.

Examples:
  python scripts/run_example.py --mode v0
  python scripts/run_example.py --mode forbid
  python scripts/run_example.py --mode soft
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_with_clingo(files: list[Path]) -> str:
    exe = shutil.which("clingo")
    if not exe:
        raise FileNotFoundError("clingo not found")
    cmd = [exe, "--opt-mode=optN", "--quiet=1"] + [str(f) for f in files]
    return subprocess.run(cmd, cwd=ROOT, text=True, stderr=subprocess.STDOUT)


def run_with_gringo_clasp(files: list[Path]) -> str:
    gringo = shutil.which("gringo")
    clasp = shutil.which("clasp")
    if not gringo or not clasp:
        raise FileNotFoundError("Neither clingo nor gringo+clasp is available")
    p1 = subprocess.Popen([gringo] + [str(f) for f in files], cwd=ROOT, stdout=subprocess.PIPE, text=True)
    p2 = subprocess.run([clasp, "--opt-mode=optN", "--quiet=1"], stdin=p1.stdout, cwd=ROOT, text=True, capture_output=True)
    if p2.returncode not in (10, 20, 30):
        raise RuntimeError(p2.stderr)
    return p2.stdout


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["v0", "forbid", "soft"], default="v0")
    parser.add_argument("--facts", default="examples/toy.lp")
    args = parser.parse_args()

    if args.mode == "v0":
        files = [Path("encodings/aspknn_v0.lp"), Path(args.facts)]
    elif args.mode == "forbid":
        files = [Path("encodings/aspknn_forbid.lp"), Path(args.facts), Path("examples/toy_forbid.lp")]
    else:
        files = [Path("encodings/aspknn_soft.lp"), Path(args.facts), Path("examples/soft_mode.lp")]

    try:
        output = run_with_clingo(files)
    except FileNotFoundError:
        output = run_with_gringo_clasp(files)

    print(output)


if __name__ == "__main__":
    main()
