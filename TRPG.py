#!/usr/bin/env python3

from rich.console import Console
from rich.panel import Panel
import os
import time
import sys

sys.path.append("Characters")
try:
    import character_creator as cc
except ModuleNotFoundError:
    print("Couldn't find the character creator function, closing the game...")
    time.sleep(2)
    sys.exit()


class Menu:
    def __init__(self, text, options):
        self.text = text
        self.options = options

    def print_menu(self, console, numbered_choices=False):
        console.print(Panel(self.text, expand=False))
        for option in self.options:
            if numbered_choices is True:
                console.print(
                    str(int(option) + 1) + ". " + self.options[option].split(":")[0]
                )
            else:
                console.print("- " + self.options[option].split(":")[0])

    def choice(self, console, numbered_choices=False):
        console.print("\n")
        if numbered_choices is True:
            console.print(" What would you like to do? (Choose a number)")
        else:
            joined_options = "("
            for option in self.options:
                joined_options = joined_options + "/" + option
            joined_options = joined_options + ")"
            joined_options = joined_options.replace("(/", "(")
            console.print(" What would you like to do? " + joined_options)

        choice_received = False
        while choice_received is False:

            choice = console.input(" Your choice: ")
            if numbered_choices is True:
                choice = int(choice) - 1

            if choice in self.options:
                choice_received = True
            else:
                console.print(" That's not a valid choice, try again...")
                time.sleep(1.0)

        return choice


class Encounter(Menu):
    def __init__(self, name, text, options):
        self.name = name
        Menu.__init__(self, text, options)

    def resolve_encounter(self, console):
        os.system("clear")
        self.print_menu(console, numbered_choices=True)
        choice = self.choice(console, numbered_choices=True)

        next_encounter = self.options[choice].split(":")[1].strip("\n ")

        return next_encounter


class Character:
    def __init__(self, name, stength, agility, intelligence, charisma):
        self.name = name
        self.stength = stength
        self.agility = agility
        self.intelligence = intelligence
        self.charisma = charisma


def read_adventure(adventure_file):
    f = open(("Adventures/" + adventure_file), mode="r")
    lines = f.readlines()
    encounters = {}

    current_line_number = 0
    adventure_finished = False
    while adventure_finished is False:
        line = lines[current_line_number]
        if line.split(":")[0] == "*encounter*":
            name = line.split(":")[1].strip("\n ")
            description = ""
            description_finished = False
            while description_finished is False:
                current_line_number = current_line_number + 1
                line = lines[current_line_number]
                if line != "*options*\n":
                    description = description + line
                else:
                    description_finished = True
                    description = description[:-1]

            options = []
            options_finished = False
            while options_finished is False:
                current_line_number = current_line_number + 1
                line = lines[current_line_number]
                if (line != "*end*\n") & (line != "*end*"):
                    options.append(line)
                else:
                    options_finished = True

            options = dict(enumerate(options))
            encounters[name] = Encounter(name, description, options)

        current_line_number = current_line_number + 1
        if current_line_number >= len(lines):
            adventure_finished = True

    f.close()
    return encounters


def choose_adventure(console):
    adventure_list = [f for f in os.listdir("Adventures") if f.endswith("txt")]
    text = "Which adventure are you taking today?"
    options = dict(enumerate(adventure_list))
    options[len(adventure_list)] = "Return"

    adventure_menu = Menu(text, options)
    adventure_menu.print_menu(console, numbered_choices=True)
    choice = adventure_menu.choice(console, numbered_choices=True)

    if choice == (len(adventure_list)):
        initialize_game(console)
    else:
        adventure = read_adventure(adventure_list[choice])

    return adventure


def read_character(name):
    f = open(("Characters/" + name), mode="r")
    attributes = []
    for attribute in f.readlines():
        attributes.append(int(attribute))

    hero = Character(
        name.split(".")[0], attributes[0], attributes[1], attributes[2], attributes[3]
    )

    return hero


def choose_character(console):
    character_list = [f for f in os.listdir("Characters") if f.endswith("txt")]
    os.system("clear")
    text = "Choose your character:"
    options = dict(enumerate(character_list))
    options[len(character_list)] = "Return"

    character_menu = Menu(text, options)
    character_menu.print_menu(console, numbered_choices=True)
    choice = character_menu.choice(console, numbered_choices=True)

    if choice == (len(character_list)):
        initialize_game(console)
    else:
        character = read_character(character_list[choice])

    return character


def initialize_game(console):
    text = (
        "[bold red]Welcome, adventurer! Are you ready for your next challenge?\n"
        "The world out there is full of monsters and treasures, and "
        "they are both waiting for you!\n"
        "Remember: Your choices always matter, so choose wisely."
    )

    options = {
        "create": "Create a character",
        "start": "Start an adventure",
        "exit": "Exit",
    }

    os.system("clear")

    starting_menu = Menu(text, options)
    starting_menu.print_menu(console)
    choice = starting_menu.choice(console)

    if choice == "create":
        os.system("clear")
        character = cc.create_character(save_folder="Characters/")
        initialize_game(console)
    elif choice == "start":
        if len(os.listdir("Characters")) > 0:
            character = choose_character(console)
            console.print("\n")
            adventure = choose_adventure(console)
        elif len(os.listdir("Characters")) == 0:
            print(
                "Looks like you have not created any characters yet,"
                " try doing that first"
            )
            time.sleep(2)
            initialize_game(console)
    elif choice == "exit":
        print("Very well, see you next time, adventurer!")
        time.sleep(2)
        sys.exit()

    return character, adventure


def main_game():
    console = Console()
    character, adventure = initialize_game(console)
    exit_game = False
    current_encounter = "first_encounter"
    while exit_game is False:
        current_encounter = adventure[current_encounter].resolve_encounter(console)


main_game()
