#!/usr/bin/env python3

import os
from rich.text import Text
import json
import random
import time


def create_character(rolls=3, save_folder=""):
    print(
        "Welcome to the character creator! First things first, what's your hero's name?"
    )
    name = input()

    attributes_accepted = False
    roll = 1

    while (attributes_accepted is False) & (roll <= rolls):
        attributes = {"strength": 0, "agility": 0, "intelligence": 0, "charisma": 0}
        index = 0
        for attribute in attributes:
            index = index + 1
            print(
                "Let's roll some dice and find out "
                + name
                + "'s attributes"
                + "." * index,
                end="\r",
            )
            attributes[attribute] = random.randint(3, 10)
            time.sleep(0.5)

        attributes["hp"] = attributes["strength"] * 10
        attributes["defense"] = max(attributes["strength"], attributes["agility"]) + 5

        print("\nYour adventurer is ready! Their attributes are (from 3 to 10):")
        print("- Stength: " + str(attributes["strength"]))
        print("- Agility: " + str(attributes["agility"]))
        print("- Intelligence: " + str(attributes["intelligence"]))
        print("- Charisma: " + str(attributes["charisma"]) + "\n")
        print("- HP (Strength * 10): " + str(attributes["hp"]))
        print("- Defense (max(str/agi) + 5): " + str(attributes["defense"]) + "\n")

        if roll < rolls:
            choice = input(
                "Would you like to roll again? You have "
                + str(rolls - roll)
                + " more chance(s) (yes/no) \n"
            ).lower()
        elif roll == rolls:
            print("You're out of chances")
            choice = "no"

        if choice == "no":
            print("Very well, your character was created!")
            print("Returning to the starting menu...")

            attributes["name"] = name
            f = open((save_folder + name + ".json"), mode="w")
            json.dump(attributes, f, indent=4, ensure_ascii=False)
            f.close

            time.sleep(3.0)
            attributes_accepted = True
        elif choice == "yes":
            roll = roll + 1
        else:
            print("That's not a valid choice, try again...")
            time.sleep(2)


def read_character(name):
    import TRPG

    f = open(("Characters/" + name + ".json"), mode="r")
    attributes = json.load(f)

    character = TRPG.Character(
        attributes["name"],
        attributes["strength"],
        attributes["agility"],
        attributes["intelligence"],
        attributes["charisma"],
        attributes["hp"],
        attributes["defense"],
    )

    return character


def choose_character(game_state, console, character_list, game_window):
    import TRPG

    os.system("clear")

    text = Text("Choose your character:", justify="center")
    options = dict(enumerate(character_list))

    character_menu = TRPG.Menu(text, options, console, game_window)
    character_menu.print_menu()
    character_menu.print_options()
    choice = character_menu.choice()

    character = read_character(character_list[choice])
    game_state.character = character
