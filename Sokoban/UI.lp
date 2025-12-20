%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%% not used in final project%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
cell(X,Y) :- coordinate(X,Y).

player_at(X,Y,0) :- on(X,Y,p,0).
box_at(X,Y,0)    :- crate(C), on(X,Y,C,0).
target(X,Y)      :- isgoal(X,Y).

% Symbol paths
asset(block,  "../elements/block.png").
asset(crate,  "../elements/crate.png").
asset(floor,  "../elements/floor.png").
asset(goal,   "../elements/goal.png").
asset(player, "../elements/player.png").

% Symbols assigned
sprite(X,Y,S) :- wall(X,Y),                asset(block,S).
sprite(X,Y,S) :- player_at(X,Y,0),         asset(player,S).
sprite(X,Y,S) :- box_at(X,Y,0),            asset(crate,S).
sprite(X,Y,S) :- target(X,Y),              asset(goal,S).
sprite(X,Y,S) :- cell(X,Y),                asset(floor,S).

elem(window, window, root).
attr(window, child_layout, grid).
attr(window, class, ("p-2";"justify-content-start")).

% Title
elem(title, label, window).
attr(title, label, "Sokoban").
attr(title, grid_column, 0).
attr(title, grid_column_span, 20).
attr(title, grid_row, 0).
attr(title, class, ("fw-bold";"mb-2")).

% Board cells
elem(cell(X,Y), container, window) :- cell(X,Y).
attr(cell(X,Y), grid_column, X) :- cell(X,Y).
attr(cell(X,Y), grid_row, Y+1)  :- cell(X,Y).

attr(cell(X,Y), width, 40)  :- cell(X,Y).
attr(cell(X,Y), height, 40) :- cell(X,Y).

attr(cell(X,Y), class, ("d-flex";"align-items-center";"justify-content-center")) :- cell(X,Y).

% Tile renderer (canvas with image attribute)
elem(tile(X,Y), canvas, cell(X,Y)) :- cell(X,Y).

attr(tile(X,Y), width, 40)  :- cell(X,Y).
attr(tile(X,Y), height, 40) :- cell(X,Y).

attr(tile(X,Y), image, S) :- cell(X,Y), sprite(X,Y,S).

% Buttons
elem(ctrls, container, window).
attr(ctrls, child_layout, grid).
attr(ctrls, grid_column, 0).
attr(ctrls, grid_column_span, 20).
attr(ctrls, grid_row, 10).
attr(ctrls, class, ("mt-3";"gap-2";"justify-content-center")).

elem(btn_up, button, ctrls).
attr(btn_up, label, "↑").
attr(btn_up, grid_column, 1).
attr(btn_up, grid_row, 0).
when(btn_up, click, call, add_assumption(ui(up), true)).

elem(btn_left, button, ctrls).
attr(btn_left, label, "←").
attr(btn_left, grid_column, 0).
attr(btn_left, grid_row, 1).
when(btn_left, click, call, add_assumption(ui(left), true)).

elem(btn_right, button, ctrls).
attr(btn_right, label, "→").
attr(btn_right, grid_column, 2).
attr(btn_right, grid_row, 1).
when(btn_right, click, call, add_assumption(ui(right), true)).

elem(btn_down, button, ctrls).
attr(btn_down, label, "↓").
attr(btn_down, grid_column, 1).
attr(btn_down, grid_row, 2).
when(btn_down, click, call, add_assumption(ui(down), true)).

#show elem/3.
#show attr/3.
#show when/4.
