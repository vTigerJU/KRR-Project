# final Mini-Project : Group 3
# written By: Axel Lindh - Hannan Khalil - Emil Anderö - Viktor Tiger 

# Sokoban with ASP-Based Hint System

import subprocess
import tempfile
import os
import sys


BASE_LP_FILE = "sokoban_base.lp"
LEVEL_FILES  = ["Apple_tree.txt", "Indestructible_Word_Game.txt", "Menorah.txt"]


def load_level_from_file(path):
    """
    load a sokoban level from a text file using classic sokoban symbols:

    supported characters:

    # = wall

    $ = box

    . = goal

    @ = player

    * = box on goal

    + = player on goal

    space = empty floor

    lines starting with 'Title' are ignored.

    """