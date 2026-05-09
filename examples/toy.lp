% Toy example from the manuscript methodology section
k(3).

train(p1). label(p1,setosa).
train(p2). label(p2,setosa).
train(p3). label(p3,versicolor).
train(p4). label(p4,versicolor).
train(p5). label(p5,virginica).

query(q1).
query(q2).

distance(q1,p1,50). distance(q1,p2,52).
distance(q1,p3,70). distance(q1,p4,75).
distance(q1,p5,90).

distance(q2,p1,80). distance(q2,p2,82).
distance(q2,p3,45). distance(q2,p4,48).
distance(q2,p5,60).
