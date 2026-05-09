% ============================================================
% aspknn_forbid.lp
% Constraint-aware ASP-KNN with query-specific forbidden labels.
% This module implements argmax and tie-breaking over allowed labels.
% ============================================================

#include "aspknn_core.lp".

% Allowed labels for each query = all labels minus forbidden ones
allowed_label(X,L) :- query(X), class(L), not forbid(X,L).

% Integrity constraint: forbidden labels must not be assigned
:- forbid(X,L), assigned_label(X,L).

% Argmax within the allowed set
higher_vote_allowed(X,C) :-
    votes(X,L1,C1), allowed_label(X,L1),
    votes(X,L2,C),  allowed_label(X,L2),
    C1 > C.

max_vote_allowed(X,C) :-
    votes(X,L,C), allowed_label(X,L),
    not higher_vote_allowed(X,C).

% Lexicographic tie-breaking restricted to allowed labels
prefer_tie_allowed(X,L) :-
    votes(X,L,C),  allowed_label(X,L),
    votes(X,L2,C), allowed_label(X,L2),
    L2 < L.

% Final assignment: choose the best label among allowed labels
assigned_label(X,L) :-
    votes(X,L,C), allowed_label(X,L),
    max_vote_allowed(X,C),
    not prefer_tie_allowed(X,L).

% Sanity check: infeasible only if no allowed label remains
:- query(X), not allowed_label(X,_).
:- query(X), not assigned_label(X,_).
:- assigned_label(X,L1), assigned_label(X,L2), L1 != L2.
