% ============================================================
% aspknn_soft.lp
% Soft-preference ASP-KNN.
% Two-level optimization aligned with the manuscript:
%   Level-2: minimize label-neighbor mismatches.
%   Level-1: minimize the farthest supporting-neighbor distance
%            of the predicted label.
% ============================================================

#include "aspknn_core.lp".

% Choose exactly one assigned label among max-vote candidate labels.
% This preserves the KNN majority-vote structure while allowing the
% optimizer to refine ambiguous/tied neighborhoods.
1 { assigned_label(X,L) : candidate_label(X,L) } 1 :- query(X).

% Level-2: minimize mismatches between assigned label and neighbor labels
:~ enable(soft), assigned_label(X,L), neighbor(X,Y), label(Y,L2), L != L2. [1@2,X,Y]

% Supporting distances for the assigned label
support_dist(X,L,D) :-
    assigned_label(X,L), neighbor(X,Y), label(Y,L), distance(X,Y,D).

% Identify the farthest supporting neighbor distance
smaller_support(X,L,D) :- support_dist(X,L,D2), support_dist(X,L,D), D2 < D.
max_support_dist(X,L,D) :- support_dist(X,L,D), not smaller_support(X,L,D).

% Level-1: minimize farthest supporter distance
:~ enable(soft), max_support_dist(X,L,D). [D@1,X,L]

:- query(X), not assigned_label(X,_).
:- assigned_label(X,L1), assigned_label(X,L2), L1 != L2.
