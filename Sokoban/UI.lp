% ==============================
% Sokoban UI for clinguin
% ==============================

% Root window
elem(window, window, root).
attr(window, child_layout, grid).
attr(window, class, ("justify-content-start")).

% Optional title row
elem(title, label, window).
attr(title, label, "Sokoban").
attr(title, grid_column, 1).
attr(title, grid_column_span, 7).
attr(title, grid_row, 0).
attr(title, class, ("fw-bold";"mb-2")).

% Board cells (as containers in a grid)
elem(cell(X,Y), container, window) :- cell(X,Y).
attr(cell(X,Y), grid_column, X) :- cell(X,Y).
attr(cell(X,Y), grid_row, Y+1) :- cell(X,Y).  % +1 because row 0 is the title

attr(cell(X,Y), width, 40) :- cell(X,Y).
attr(cell(X,Y), height, 40) :- cell(X,Y).
attr(cell(X,Y), class,
     ("border";"border-dark";"d-flex";"align-items-center";"justify-content-center")) :-
    cell(X,Y).

% Background coloring depending on content
attr(cell(X,Y), class, ("bg-secondary";"bg-opacity-50")) :- wall(X,Y).
attr(cell(X,Y), class, ("bg-warning";"bg-opacity-50")) :- target(X,Y), not box(X,Y).
attr(cell(X,Y), class, ("bg-success";"bg-opacity-50")) :- box_on_target(X,Y).
attr(cell(X,Y), class, ("bg-info";"bg-opacity-50")) :- player(X,Y).

% ---------------------------
% Symbols inside each cell
% ---------------------------

% We build a symbol/3 predicate to avoid conflicting label attrs

symbol(X,Y,"#") :- wall(X,Y).
symbol(X,Y,"@") :- player(X,Y), not target(X,Y).
symbol(X,Y,"$") :- box(X,Y), not target(X,Y).
symbol(X,Y,"*") :- box_on_target(X,Y).
symbol(X,Y,".") :- target(X,Y), not box(X,Y).
symbol(X,Y," ") :-
    cell(X,Y),
    not wall(X,Y),
    not box(X,Y),
    not target(X,Y),
    not player(X,Y).

elem(label(X,Y), label, cell(X,Y)) :- symbol(X,Y,_).
attr(label(X,Y), label, S) :- symbol(X,Y,S).
attr(label(X,Y), class, ("fw-bold";"text-center")) :- symbol(X,Y,_).

% No interactions yet (when/4) – just a viewer
% Control panel container (under the window)
elem(ctrls, container, window).
attr(ctrls, child_layout, flex).
attr(ctrls, class, ("mt-2";"gap-2")).

% Up button
elem(btn_up, button, ctrls).
attr(btn_up, label, "↑").
when(btn_up, click, call, add_assumption(move(up), true)).

% Left button
elem(btn_left, button, ctrls).
attr(btn_left, label, "←").
when(btn_left, click, call, add_assumption(move(left), true)).

% Right button
elem(btn_right, button, ctrls).
attr(btn_right, label, "→").
when(btn_right, click, call, add_assumption(move(right), true)).

% Down button
elem(btn_down, button, ctrls).
attr(btn_down, label, "↓").
when(btn_down, click, call, add_assumption(move(down), true)).
