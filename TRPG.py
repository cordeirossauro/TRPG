#!/usr/bin/env python3

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.columns import Columns
import os
import random
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
        console.print(Panel(self.text, width=64))
        for option in self.options:
            if numbered_choices is True:
                console.print(
                    str(int(option) + 1) + ". " + self.options[option].split(":")[0]
                )
            else:
                console.print("- " + self.options[option].split(":")[0])

    def choice(self, console, numbered_choices=False):
        if numbered_choices is True:
            console.print("\n What would you like to do? (Choose a number)")
        else:
            joined_options = "("
            for option in self.options:
                joined_options = joined_options + "/" + option
            joined_options = joined_options + ")"
            joined_options = joined_options.replace("(/", "(")
            console.print("\n What would you like to do? " + joined_options)

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

    def resolve_encounter(self, character, console):
        os.system("clear")
        self.print_menu(console, numbered_choices=True)
        choice = self.choice(console, numbered_choices=True)

        result = self.options[choice].split(":")[1]
        if len(result.split(",")) == 1:
            next_encounter = result.strip("\n ")
        else:
            enemy = read_character(result.split(",")[0].strip(" "))

            battle = Battle(character, enemy)
            game_over = battle.resolve_battle(console)
            if game_over is True:
                next_encounter = 0
            else:
                next_encounter = result.split(",")[1].strip("\n ")
                del self.options[choice]

        return next_encounter


class Character:
    def __init__(self, name, strength, agility, intelligence, charisma, hp, defense):
        self.name = name
        self.strength = strength
        self.agility = agility
        self.intelligence = intelligence
        self.charisma = charisma
        self.hp = hp
        self.defense = defense

    def attack(self, enemy, battle_log, console, turn):
        roll = random.randint(1, 6) + random.randint(1, 6) + self.strength
        if (roll) > enemy.defense:
            console.print(
                " " + self.name + "'s attacking roll: " + str(roll) + " (success)"
            )
            damage = self.strength
            enemy.hp = enemy.hp - damage
            battle_log.append(
                "Turn "
                + str(turn)
                + ": "
                + self.name
                + " attacked "
                + enemy.name
                + " for "
                + str(damage)
                + " damage.\n"
            )
        else:
            console.print(
                " " + self.name + "'s attacking roll: " + str(roll) + " (fail)"
            )
            battle_log.append(
                "Turn "
                + str(turn)
                + ": "
                + self.name
                + " attacked "
                + enemy.name
                + " but couldn't hit. \n"
            )


class Battle(Menu):
    def __init__(self, character, enemy):
        self.character = character
        self.enemy = enemy
        self.battle_log = []
        Menu.__init__(self, "", {"attack": "Attack your enemy", "flee": "Try to flee"})

    def make_sheet(self, character):
        sheet = Text()
        sheet.append(Text("- Strength:             " + str(character.strength)))
        sheet.append(Text("\n- Agility:              " + str(character.agility)))
        sheet.append(Text("\n- Intelligence:         " + str(character.intelligence)))
        sheet.append(Text("\n- Charisma:             " + str(character.charisma)))
        sheet.append(Text("\n- HP:                   " + str(character.hp)))
        sheet.append(Text("\n- Defense:              " + str(character.defense)))

        return sheet

    def print_details(self, console):
        character_sheet = self.make_sheet(self.character)
        enemy_sheet = self.make_sheet(self.enemy)

        columns = Columns(
            [
                Panel(character_sheet, title=self.character.name),
                Panel(enemy_sheet, title=self.enemy.name),
            ],
            width=30,
        )

        console.print(Panel(Text("Battle", justify="center"), width=62))
        console.print(columns)
        console.print(
            Panel("".join(self.battle_log[-6:]), title="Battle Log", width=62, height=8)
        )

    def roll_initiative(self):
        draw = True

        while draw is True:
            character_initiative = random.randint(1, 6) + self.character.agility
            enemy_initiative = random.randint(1, 6) + self.enemy.agility

            if character_initiative > enemy_initiative:
                winner = self.character.name
                draw = False
                enemy_won_roll = False
            elif character_initiative < enemy_initiative:
                winner = self.enemy.name
                draw = False
                enemy_won_roll = True

        self.battle_log.append(winner + " takes the initiative... \n")
        return enemy_won_roll

    def resolve_battle(self, console):
        battle_finished = False
        enemy_won_roll = self.roll_initiative()
        turn = 0

        while battle_finished is False:
            os.system("clear")
            turn = turn + 1
            self.print_details(console)
            choice = self.choice(console)
            console.print("")
            if choice == "attack":
                if enemy_won_roll is True:
                    self.enemy.attack(self.character, self.battle_log, console, turn)
                    time.sleep(1.0)
                    self.character.attack(self.enemy, self.battle_log, console, turn)
                    time.sleep(1.5)
                else:
                    self.character.attack(self.enemy, self.battle_log, console, turn)
                    time.sleep(1.0)
                    self.enemy.attack(self.character, self.battle_log, console, turn)
                    time.sleep(1.5)

            elif choice == "flee":
                battle_finished = True

            if self.enemy.hp <= 0:
                os.system("clear")
                self.print_details(console)
                console.print(
                    "[bold yellow]\n You won the battle! Your enemy "
                    "lays dead before you..."
                )
                input(" Press Enter to continue...")
                battle_finished = True
                game_over = False
            elif self.character.hp <= 0:
                os.system("clear")
                self.print_details(console)
                console.print(
                    "[bold red]\n Even with all your might, this enemy "
                    "proved too powerful for you.\n Your adventure "
                    "ends here..."
                )
                input(" Press Enter to continue...")
                battle_finished = True
                game_over = True

        return game_over


def read_adventure(adventure_file):
    f = open(("Adventures/" + adventure_file + ".txt"), mode="r")
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
    adventure_list = [
        f.split(".")[0] for f in os.listdir("Adventures") if f.endswith("txt")
    ]
    text = Text("Which adventure are you taking today?", justify="center")
    options = dict(enumerate(adventure_list))
    options[len(adventure_list)] = "Return"

    adventure_menu = Menu(text, options)
    adventure_menu.print_menu(console, numbered_choices=True)
    choice = adventure_menu.choice(console, numbered_choices=True)

    if choice == (len(adventure_list)):
        character, adventure = initialize_game(console)
    else:
        adventure = read_adventure(adventure_list[choice])

    return adventure


def read_character(name):
    f = open(("Characters/" + name + ".txt"), mode="r")
    attributes = []
    for attribute in f.readlines():
        attributes.append(int(attribute))

    hero = Character(
        name.split(".")[0],
        attributes[0],
        attributes[1],
        attributes[2],
        attributes[3],
        attributes[4],
        attributes[5],
    )

    return hero


def choose_character(console):
    character_list = [
        f.split(".")[0] for f in os.listdir("Characters") if f.endswith("txt")
    ]
    os.system("clear")
    text = Text("Choose your character:", justify="center")
    options = dict(enumerate(character_list))

    character_menu = Menu(text, options)
    character_menu.print_menu(console, numbered_choices=True)
    choice = character_menu.choice(console, numbered_choices=True)

    character = read_character(character_list[choice])

    return character


def initialize_game(console):
    text = (
        "[bold red]Welcome, adventurer! Are you ready for your next challenge?\n"
        "The world out there is full of monsters and treasures, and\n"
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
    next_encounter = "first_encounter"
    while exit_game is False:
        next_encounter = adventure[next_encounter].resolve_encounter(character, console)
        if next_encounter == 0:
            exit_game = True


main_game()
