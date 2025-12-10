% UI.lp
elem(w, window, root).
elem(b1, button, w).
attr(b1, label, "Hello world button").
when(b1, click, call, next_solution).
