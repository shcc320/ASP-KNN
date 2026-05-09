% ============================================================
% aspknn_v0.lp
% Baseline ASP-KNN with deterministic lexicographic tie-breaking.
% Matches the baseline formulation P0 in the manuscript.
% ============================================================

#include "aspknn_core.lp".

% Deterministic tie-breaking among max-vote labels
prefer_tie(X,L) :- candidate_label(X,L), candidate_label(X,L2), L2 < L.
assigned_label(X,L) :- candidate_label(X,L), not prefer_tie(X,L).

% Safety: every query receives exactly one label.
:- query(X), not assigned_label(X,_).
:- assigned_label(X,L1), assigned_label(X,L2), L1 != L2.
