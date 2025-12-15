% final Mini-Project : Group 3
% written By: Axel Lindh - Hannan Khalil - Emil Anderö - Viktor Tiger 

% Sokoban with ASP-Based Hint System


#const maxT = 200. %we can change later if we need it


time(0..maxT).
dir(up; down; left; right).


%---At each time step choose exactly one move-----

1 { move(D, T) : dir(D) } 1 :- time (T), T < maxT.

%---helper: cell occupied by a box at time T -----

box_at(X, Y, T) :- box(B, X, Y, T).

occupied(X, Y, T) :- wall(X, Y).
occupied(X, Y, T) :-box_at(X, Y, T).


%--- Player movement -----

next_pos (X, Y, up, X, Y1)     :- Y1 = Y - 1.
next_pos (X, Y, down, X, Y1)   :- Y1 = Y + 1.
next_pos (X, Y, left, X, Y1)   :- X1 = X - 1.
next_pos (X, Y, right, X, Y1)  :- X1 = X - 1.

%--- move without box-----
player (X2, Y2, T + 1) :- 
                player (X, Y, T),
                move (D, T),
                next_pos (X, Y, D, X2, Y2),
                x(X2),  y(Y2),
                not box_at (X2, Y2, T),
                not wall (X2, Y2). 


%--- beyond position (for pushing)-----
beyond_pos(X, Y, up, X, Y2)    :- Y2 = Y - 1.
beyond_pos(X, Y, down, X, Y2)  :- Y2 = Y + 1.
beyond_pos(X, Y, left, X2, Y)  :- X2 = X - 1.
beyond_pos(X, Y, right, X2, Y) :- X2 = X + 1.



%---pushing rule: player and box move together
player (Xb, Yb, T + 1) :- 
            player (X, Y, T),
            move(D, T),
            next_pos(X, Y, D, Xb, Yb),
            box(B, Xb, Yb, T),
            beyond_pos(Xb, Yb, D, Xb2, Yb2),
            x(Xb2), y(Yb2),
            not occupied(Xb2, Yb2, T).


box (B, Xb2, Yb2, T + 1) :-
            player(X, Y, T),
            move(D, T),
            next_pos(X, Y, D, Xb, Yb),
            box(B, Xb, Yb, T),
            beyond_pos(Xb, Yb, D, Xb2, Yb2),
            x(Xb2), y(Yb2),
            not occupied(Xb2, Yb2, T).


%--- Frame axioms (Boxes that are not pushed stay)-----

move_box (B, T) :- 
        box(B, X, Y, T),
        player(PX, PY, T),
        move(D, T),
        next_pos(PX, PY, D, X, Y).


box (B, X, Y, T+1) :- 
    box(B, X, Y, T),
    not moved_box(B, T).


%--- Illegal moves -----

% cannot move outside grid
:- move (D, T), player (X, Y, T),
    next_pos(X, Y, D, X2, Y2),
    (not x(X2); not y(Y2)).


% cannot walk into a wall directly
:- move (D, T), player (X, Y, T),
    next_pos(X, Y, D, X2, Y2),
    wall(X2, Y2),
    not box_at(X2, Y2, T).

% cannot push box into wall or another box or outside grid
:- move (D, T), player (X, Y, T),
    next_pos(X, Y, D, X2, Y2),
    box(B, Xb, Yb, T),
    ( not beyond_pos(Xb, Yb, D, Xb2, Yb2)
    ; not x(Xb2)
    ; not y(Yb2)
    ; wall(Xb2, Yb2)
    ; box_at(Xb2, Yb2, T)).



%--- Initial conditions -----
% exactly one player at time 0

:- not 1 { player (X, Y, 0) : x(X), y(Y) } 1.

%--- Goal condition-----
all_boxes_on_goals(T) :-
    time(T),
    not bad_box(T).


bad_box(T) :- 
    box(B, X, Y, T),
    not goal(X, Y).


solved :- all_boxes_on_goals(T).
:- not solved.



#minimize { 1, T : move(_, T) }.


%---OutPut------
#show move/2.
