wall(0,0).
wall(0,1).
wall(0,2).
wall(0,3).
wall(0,4).
wall(1,0).
wall(2,0).
wall(3,0).
wall(4,0).

wall(4,1).
wall(4,2).
wall(4,3).
wall(4,4).
wall(1,4).
wall(2,4).
wall(3,4).

crate(c).
on(2,2,c,0).
player(p).
on(2,3,p,0).
isgoal(2,1).

coordinate(X,Y) :- X = 0..5, Y = 0..5.