#!/usr/bin/env python3

import os
from rich.text import Text
import joblib as jb


def save_game(game_state, console):
    file_name = console.input(" Name for the save file: ")
    jb.dump(game_state, open(("Saves/" + file_name + ".sav"), "wb"), compress=9)


def choose_save(game_state, console, save_list, game_window):
    import TRPG

    os.system("clear")

    text = Text("Choose the game to load:", justify="center")
    options = dict(enumerate(save_list))

    save_menu = TRPG.Menu(text, options, console, game_window)
    save_menu.print_menu(console, numbered_choices=True)
    save_menu.print_options()
    choice = save_menu.choice(console, numbered_choices=True)

    loaded_game_state = jb.load(open(("Saves/" + options[choice] + ".sav"), "rb"))

    game_state.adventure = loaded_game_state.adventure
    game_state.character = loaded_game_state.character
    game_state.next_encounter = loaded_game_state.next_encounter
