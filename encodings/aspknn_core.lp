% ============================================================
% aspknn_core.lp
% Shared ASP-KNN core: candidate generation, stable ranking,
% top-k neighbor selection, vote aggregation, and explanations.
% ============================================================

% Class domain
class(L) :- label(_,L).

% Candidate neighbors
knn(X,Y,D) :- query(X), train(Y), distance(X,Y,D).

% Distance ordering relations
lt(X,A,B)  :- knn(X,A,DA), knn(X,B,DB), DA < DB.
eqd(X,A,B) :- knn(X,A,D),  knn(X,B,D),  A != B.

% Stable rank computation. R is zero-based.
rank(X,Y,R) :-
    knn(X,Y,_),
    R1 = #count{Z : lt(X,Z,Y)},
    R2 = #count{Z : eqd(X,Z,Y), Z < Y},
    R  = R1 + R2.

% Top-k neighbor selection
neighbor(X,Y) :- rank(X,Y,R), k(K), R < K.

% Vote aggregation per label
votes(X,L,C) :-
    query(X),
    class(L),
    C = #count{Y : neighbor(X,Y), label(Y,L)}.

% Identification of maximal vote counts
higher_vote(X,C) :- votes(X,_,C2), votes(X,_,C), C2 > C.
max_vote(X,C) :- votes(X,_,C), not higher_vote(X,C).

% Candidate labels with maximal vote count
candidate_label(X,L) :- votes(X,L,C), max_vote(X,C).

% Explanation predicates
support(X,Y,L) :- neighbor(X,Y), label(Y,L).
majority_evidence(X,L,Y) :- assigned_label(X,L), support(X,Y,L).

#show assigned_label/2.
#show neighbor/2.
#show votes/3.
#show support/3.
#show majority_evidence/3.
