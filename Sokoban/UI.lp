% Root window
elem(win, window, root).
attr(win, title, "Hello clinguin").

% Label inside the window
elem(lbl, label, win).
attr(lbl, text, "Hello, world from clinguin!").
