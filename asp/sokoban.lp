#const maxT = 50.
time(0..maxT).
final(maxT).

goal_reached :- 
    final(T),
    #count { C,X,Y : crate(C), on(X,Y,C,T), isgoal(X,Y) } = N,
    N = #count { C : crate(C) }.

:- not goal_reached.

occupied(X,Y,T) :- on(X,Y,_,T).

%%%Integrity constraints%%%
%Player can't be in two locations at once
:- player(p), on(X1,Y1,p,T), on(X2,Y2,p,T), X1 != X2, Y1 != Y2.
%Crates can't be in two locations at once
:- crate(C), on(X1,Y1,C,T), on(X2,Y2,C,T), X1 != X2, Y1 != Y2.
%Crates can't be stacked
:- crate(C1), crate(C2), C1 != C2, on(X,Y,C1,T), on(X,Y,C2,T).
%Player and crate can't share a tile
:- crate(C), player(p), on(X,Y,C,T), on(X,Y,p,T).

%Corners where boxes get stuck
deadlock(X,Y) :- not isgoal(X,Y), wall(X-1,Y), wall(X,Y-1).
deadlock(X,Y) :- not isgoal(X,Y), wall(X-1,Y), wall(X,Y+1).
deadlock(X,Y) :- not isgoal(X,Y), wall(X+1,Y), wall(X,Y-1).
deadlock(X,Y) :- not isgoal(X,Y), wall(X+1,Y), wall(X,Y+1).

%%%Action Selection%%%
{do(M,T) : move(M)} <= 1 :- time(T), T < maxT.

%%%Possible actions%%%
%Move
move(moveLeft(p,X,Y)) :- player(p), coordinate(X,Y).
move(moveRight(p,X,Y)) :- player(p), coordinate(X,Y).
move(moveDown(p,X,Y)) :- player(p), coordinate(X,Y).
move(moveUp(p,X,Y)) :- player(p), coordinate(X,Y).
%Push
move(pushLeft(p,X,Y,C)) :- player(p), crate(C), coordinate(X,Y).
move(pushRight(p,X,Y,C)) :- player(p), crate(C), coordinate(X,Y).
move(pushDown(p,X,Y,C)) :- player(p), crate(C), coordinate(X,Y).
move(pushUp(p,X,Y,C)) :- player(p), crate(C), coordinate(X,Y).

%%%Inertia for crate and player%%%
on(X,Y,C,T+1) :- on(X,Y,C,T), time(T), not -on(X,Y,C,T+1).

%%%Constraints on actions%%%
%Must move into empty space
:- do(moveLeft(p,X,Y),T), occupied(X-1,Y,T).
:- do(moveRight(p,X,Y),T), occupied(X+1,Y,T).
:- do(moveDown(p,X,Y),T), occupied(X,Y+1,T).
:- do(moveUp(p,X,Y),T), occupied(X,Y-1,T).

%Must push box into empty space
:- do(pushLeft(p,X,Y,C),T), occupied(X-2,Y,T).
:- do(pushRight(p,X,Y,C),T), occupied(X+2,Y,T).
:- do(pushDown(p,X,Y,C),T), occupied(X,Y+2,T).
:- do(pushUp(p,X,Y,C),T), occupied(X,Y-2,T).

%Forbidden to move player into wall
:- do(moveLeft(p,X,Y),T), wall(X-1,Y).
:- do(moveRight(p,X,Y),T), wall(X+1,Y).
:- do(moveDown(p,X,Y),T), wall(X,Y+1).
:- do(moveUp(p,X,Y),T), wall(X,Y-1).

%Forbidden to push crate into wall
:- do(pushLeft(p,X,Y,C),T), wall(X-2,Y).
:- do(pushRight(p,X,Y,C),T), wall(X+2,Y).
:- do(pushDown(p,X,Y,C),T), wall(X,Y+2).
:- do(pushUp(p,X,Y,C),T), wall(X,Y-2).

%Forbidden to push into locked corner
:- do(pushLeft(p,X,Y,C),T), deadlock(X-2,Y).
:- do(pushRight(p,X,Y,C),T), deadlock(X+2,Y).
:- do(pushDown(p,X,Y,C),T), deadlock(X,Y+2).
:- do(pushUp(p,X,Y,C),T), deadlock(X,Y-2).

%%%Effects of Action%%%
%PushLeft
on(X-2,Y,C,T+1) :- do(pushLeft(p,X,Y,C),T),
    on(X-1,Y,C,T),
    on(X,Y,p,T).
-on(X-1,Y,C,T+1) :- do(pushLeft(p,X,Y,C),T),
    on(X-1,Y,C,T),
    on(X,Y,p,T).
on(X-1,Y,p,T+1) :- do(pushLeft(p,X,Y,C),T),
    on(X-1,Y,C,T),
    on(X,Y,p,T).
-on(X,Y,p,T+1) :- do(pushLeft(p,X,Y,C),T),
    on(X-1,Y,C,T),
    on(X,Y,p,T).
%PushRight
on(X+2,Y,C,T+1) :- do(pushRight(p,X,Y,C),T),
    on(X+1,Y,C,T),
    on(X,Y,p,T).
-on(X+1,Y,C,T+1) :- do(pushRight(p,X,Y,C),T),
    on(X+1,Y,C,T),
    on(X,Y,p,T).
on(X+1,Y,p,T+1) :- do(pushRight(p,X,Y,C),T),
    on(X+1,Y,C,T),
    on(X,Y,p,T).
-on(X,Y,p,T+1) :- do(pushRight(p,X,Y,C),T),
    on(X+1,Y,C,T),
    on(X,Y,p,T).
%PushDown
on(X,Y+2,C,T+1) :- do(pushDown(p,X,Y,C),T),
    on(X,Y+1,C,T),
    on(X,Y,p,T).
-on(X,Y+1,C,T+1) :- do(pushDown(p,X,Y,C),T),
    on(X,Y+1,C,T),
    on(X,Y,p,T).
on(X,Y+1,p,T+1) :- do(pushDown(p,X,Y,C),T),
    on(X,Y+1,C,T),
    on(X,Y,p,T).
-on(X,Y,p,T+1) :- do(pushDown(p,X,Y,C),T),
    on(X,Y+1,C,T),
    on(X,Y,p,T).
%PushUp
on(X,Y-2,C,T+1) :- do(pushUp(p,X,Y,C),T),
    on(X,Y-1,C,T),
    on(X,Y,p,T).
-on(X,Y-1,C,T+1) :- do(pushUp(p,X,Y,C),T),
    on(X,Y-1,C,T),
    on(X,Y,p,T).
on(X,Y-1,p,T+1) :- do(pushUp(p,X,Y,C),T),
    on(X,Y-1,C,T),
    on(X,Y,p,T).
-on(X,Y,p,T+1) :- do(pushUp(p,X,Y,C),T),
    on(X,Y-1,C,T),
    on(X,Y,p,T).

%MoveLeft
on(X-1,Y,p,T+1) :- do(moveLeft(p,X,Y),T),
    on(X,Y,p,T).
-on(X,Y,p,T+1) :- do(moveLeft(p,X,Y),T),
    on(X,Y,p,T).

%MoveRight
on(X+1,Y,p,T+1) :- do(moveRight(p,X,Y),T),
    on(X,Y,p,T).
-on(X,Y,p,T+1) :- do(moveRight(p,X,Y),T),
    on(X,Y,p,T).

%MoveDown
on(X,Y+1,p,T+1) :- do(moveDown(p,X,Y),T),
    on(X,Y,p,T).
-on(X,Y,p,T+1) :- do(moveDown(p,X,Y),T),
    on(X,Y,p,T).

%MoveUp
on(X,Y-1,p,T+1) :- do(moveUp(p,X,Y),T),
    on(X,Y,p,T).
-on(X,Y,p,T+1) :- do(moveUp(p,X,Y),T),
    on(X,Y,p,T).

#show do/2.
#show on/4.