% final Mini-Project : Group 3
% written By: Axel Lindh - Hannan Khalil - Emil Anderö - Viktor Tiger 

% Sokoban with ASP-Based Hint System


#const maxT = 120.
#const maxPush = 5. % can push 5 times


time(0..maxT).
dir(up; down; left; right).
pushn(0..maxPush).

%---At each time step choose exactly one move-----

{ move(D, T) : dir(D) } <= 1 :- time(T), T < maxT.

%---helpers -----

box_at(X, Y, T) :- box(B, X, Y, T).

occupied(X, Y, T) :- wall(X, Y).
occupied(X, Y, T) :-box_at(X, Y, T).


%---movement -----

next_pos (X, Y, up, X, Y1)     :- Y1 = Y-1.
next_pos (X, Y, down, X, Y1)   :- Y1 = Y+1.
next_pos (X, Y, left, X1, Y)   :- X1 = X-1.
next_pos (X, Y, right, X1, Y)  :- X1 = X+1.


beyond_pos(X, Y, up, X, Y2)    :- Y2 = Y-1.
beyond_pos(X, Y, down, X, Y2)  :- Y2 = Y+1.
beyond_pos(X, Y, left, X2, Y)  :- X2 = X-1.
beyond_pos(X, Y, right, X2, Y) :- X2 = X+1.


%--- move without box-----
player (X2,Y2,T+1) :- 
    player (X,Y,T),
    move (D,T),
    next_pos (X,Y,D,X2,Y2),
    x(X2),  y(Y2),
    not wall(X2,Y2),
    not box_at (X2,Y2,T). 


move_box(B,T) :- 
    player(PX,PY,T),
    move(D,T),
    next_pos(PX,PY,D,BX,BY),
    box(B,BX,BY,T).



%---pushing rule: player and box move together
player (Xb, Yb, T+1) :- 
            player (X, Y, T),
            move(D, T),
            next_pos(X, Y, D, Xb, Yb),
            box_at(Xb, Yb, T),
            beyond_pos(Xb, Yb, D, Xb2, Yb2),
            x(Xb2), y(Yb2),
            not occupied(Xb2, Yb2, T).


box (B, Xb2, Yb2, T+1) :-
            player(X, Y, T),
            move(D, T),
            next_pos(X, Y, D, Xb, Yb),
            box(B, Xb, Yb, T),
            beyond_pos(Xb, Yb, D, Xb2, Yb2),
            x(Xb2), y(Yb2),
            not occupied(Xb2, Yb2, T).
            push_left(B,N,T), N > 0.


box (B,X,Y,T+1) :- 
    box(B,X,Y,T),
    not moved_box(B,T).


%--- Push counter dynamics-----
push_left(B,N-1,T+1) :-
    push_left(B,N,T),
    moved_box(B,T),
    N > 0.

push_left(B,N,T+1) :-
    push_left(B,N,T),
    not moved_box(B,T).




%---Basic bounds constraints-----
:- move (D, T), player (X, Y, T),
    next_pos(X, Y, D, X2, Y2),
    (not x(X2); not y(Y2)).


:- move (D, T), player (X, Y, T),
    next_pos(X, Y, D, X2, Y2),
    wall(X2, Y2),
    not box_at(X2, Y2, T).


:- move (D, T), player (X, Y, T),
    next_pos(X, Y, D, X2, Y2),
    box_at(X2, Y2, T),
    beyond_pos(X2, Y2, D, X3, Y3)
    ( not x(X3); not y(Y3); wall(X3, Y3); box_at(X3, Y3, T)).


%--- If any box has 0 pushes left & is not on a goal -> UNSAT---

:- box(B,X,Y,T), push_left(B,0,T), not goal(X,Y).


unsolved(T) :- box(B,X,Y,T), not goal(X,Y).
solved (T) :- time(T), not unsolved(T).


:- not 1 { solved(T) : time(T) }.


%----hint: require at least one move at T = 0 ----
:- not 1 { move(_,0) }.

#minimize { T : solved (T) }.
#minimize { T : move(_, T) }.


%---OutPut------
#show move/2.
