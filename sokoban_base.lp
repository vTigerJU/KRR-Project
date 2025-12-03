% final Mini-Project : Group 3
% written By: Axel Lindh - Hannan Khalil - Emil Anderö - Viktor Tiger 

% Sokoban with ASP-Based Hint System


#const maxT = 40. %we can change later if we need it


time(0..maxT).
dir(up; down; left; right).


%---At each time step choose exactly one move-----

1 { move(D, T) : dir(D) } 1 :- time (T), T < maxT.

%---helper: cell occupied by a box at time T -----

box_at(X, Y, T) :- box(B, X, Y, T).

occupied(X, Y, T) :- wall(X, Y).
occupied(X, Y, T) :-box_at(X, Y, T).


%--- Player movement -----







%--- Initial conditions -----
% exactly one player at time 0

:- not 1 { player (X, Y, 0) : x(X), y(Y) } 1.

