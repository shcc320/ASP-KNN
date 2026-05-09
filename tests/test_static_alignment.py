"""Static checks that key ASP rules are aligned with the manuscript.

These checks do not replace solver-based testing. They guard against
accidentally publishing an LP module whose main rules differ from the
paper description.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(name: str) -> str:
    return (ROOT / name).read_text(encoding="utf-8")


def test_core_contains_stable_ranking_and_voting():
    core = read("encodings/aspknn_core.lp")
    assert "rank(X,Y,R)" in core
    assert "R1 = #count{Z : lt(X,Z,Y)}" in core
    assert "R2 = #count{Z : eqd(X,Z,Y), Z < Y}" in core
    assert "neighbor(X,Y) :- rank(X,Y,R), k(K), R < K." in core
    assert "votes(X,L,C)" in core


def test_v0_has_lexicographic_tie_breaking():
    v0 = read("encodings/aspknn_v0.lp")
    assert "prefer_tie(X,L)" in v0
    assert "L2 < L" in v0
    assert "assigned_label(X,L) :- candidate_label(X,L), not prefer_tie(X,L)." in v0


def test_forbid_restricts_argmax_to_allowed_labels():
    forbid = read("encodings/aspknn_forbid.lp")
    assert "allowed_label(X,L) :- query(X), class(L), not forbid(X,L)." in forbid
    assert ":- forbid(X,L), assigned_label(X,L)." in forbid
    assert "higher_vote_allowed" in forbid
    assert "max_vote_allowed" in forbid
    assert "prefer_tie_allowed" in forbid


def test_soft_matches_two_level_support_distance_preference():
    soft = read("encodings/aspknn_soft.lp")
    assert "[1@2,X,Y]" in soft
    assert "support_dist(X,L,D)" in soft
    assert "max_support_dist(X,L,D)" in soft
    assert "[D@1,X,L]" in soft
