%Walls around a square
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
%Extra walls
wall(2,1).

crate(c1;c2).
on(2,2,c1,0).
on(3,2,c2,0).
player(p).
on(3,3,p,0).
isgoal(1,1).
isgoal(3,1).
coordinate(X,Y) :- X = 0..10, Y = 0..10.
