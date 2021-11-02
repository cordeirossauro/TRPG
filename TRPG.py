#!/usr/bin/env python3

from pynput import keyboard

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.columns import Columns
from rich import box
import os
import random
import time
import sys
import subprocess
import re

sys.path.append("Characters")
sys.path.append("Adventures")
sys.path.append("Saves")
try:
    import characters as cha
    import adventures as adv
    import saves as sav
except ModuleNotFoundError:
    print("Couldn't find the necessary functions, closing the game...")
    time.sleep(2)
    sys.exit()


class GameState:
    def __init__(self):
        self.next_encounter = "first_encounter"
        self.game_over = False


class Menu:
    def __init__(self, text, options, console, game_window):
        self.text = text
        self.options = options
        self.current_option = 0
        self.choice_made = False
        self.console = console
        self.game_window = game_window

    def print_menu(self):
        self.console.print(Panel(self.text, width=64), justify="center")

    def print_options(self):
        current_option_key = list(self.options.keys())[self.current_option]
        options_text = ""
        for option in self.options:
            if option == current_option_key:
                options_text = options_text + "> " + self.options[option] + " <\n"
            else:
                options_text = options_text + self.options[option] + "\n"
        options_text = options_text.rstrip("\n")

        self.console.print(
            Panel(Text(options_text, justify="center"), box=box.SIMPLE, width=64),
            justify="center",
        )

    def on_press(self, key):
        if get_active_window_title() == self.game_window:
            if key == keyboard.Key.up:
                if self.current_option > 0:
                    self.current_option = self.current_option - 1
                os.system("clear")
                self.print_menu()
                self.print_options()

            elif key == keyboard.Key.down:
                if self.current_option < len(self.options) - 1:
                    self.current_option = self.current_option + 1
                os.system("clear")
                self.print_menu()
                self.print_options()

            elif key == keyboard.Key.enter:
                return False

            else:
                os.system("clear")
                self.print_menu()
                self.print_options()

    def choice(self):
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()

        return list(self.options.keys())[self.current_option]


class Encounter(Menu):
    def __init__(self, name, text, options, results, console, game_window):
        self.name = name
        self.results = results
        Menu.__init__(self, text, options, console, game_window)

    def resolve_encounter(self, game_state):
        encounter_resolved = False

        while encounter_resolved is False:
            os.system("clear")
            self.print_menu()
            self.print_options()

            choice = self.choice()

            if choice != "menu":
                result = self.results[choice]

                if len(result) == 1:
                    game_state.next_encounter = result[0]
                    encounter_resolved = True
                else:
                    enemy = cha.read_character(result[0])

                    battle = Battle(
                        game_state.character, enemy, self.console, self.game_window
                    )
                    battle.resolve_battle(game_state, self.console)
                    game_state.next_encounter = result[1]
                    del self.options[choice]
                    self.current_option = 0
                    encounter_resolved = True

            elif choice == "menu":
                game_menu(game_state, self.console, self.game_window)


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
        if self.hp > 0:
            roll = random.randint(1, 6) + random.randint(1, 6) + self.strength
            if (roll > enemy.defense) & (roll < 12 + self.strength):
                console.print(
                    " "
                    + self.name
                    + "'s attacking roll: "
                    + str(roll)
                    + "[bold green] (success)",
                    justify="center",
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

            elif roll == 12 + self.strength:
                console.print(
                    " "
                    + self.name
                    + "'s attacking roll: "
                    + str(roll)
                    + "[bold yellow] (CRITICAL)",
                    justify="center",
                )
                damage = self.strength * 2
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
                    " "
                    + self.name
                    + "'s attacking roll: "
                    + str(roll)
                    + "[bold red] (fail)",
                    justify="center",
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
        else:
            console.print(" " + self.name + " is dead.", justify="center")


class Battle(Menu):
    def __init__(self, character, enemy, console, game_window):
        self.character = character
        self.enemy = enemy
        self.battle_log = []
        Menu.__init__(
            self,
            "",
            {"attack": "Attack your enemy", "flee": "Try to flee"},
            console,
            game_window,
        )

    def make_sheet(self, character):
        sheet = Text()
        sheet.append(Text("- Strength:             " + str(character.strength)))
        sheet.append(Text("\n- Agility:              " + str(character.agility)))
        sheet.append(Text("\n- Intelligence:         " + str(character.intelligence)))
        sheet.append(Text("\n- Charisma:             " + str(character.charisma)))
        sheet.append(Text("\n- HP:                   " + str(character.hp)))
        sheet.append(Text("\n- Defense:              " + str(character.defense)))

        return sheet

    def on_press(self, key):
        if get_active_window_title() == self.game_window:
            if key == keyboard.Key.up:
                if self.current_option > 0:
                    self.current_option = self.current_option - 1
                os.system("clear")
                self.print_details()
                self.print_options()

            elif key == keyboard.Key.down:
                if self.current_option < len(self.options) - 1:
                    self.current_option = self.current_option + 1
                os.system("clear")
                self.print_details()
                self.print_options()

            elif key == keyboard.Key.enter:
                return False

            else:
                os.system("clear")
                self.print_details()
                self.print_options()

    def choice(self, numbered_choices=False):
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()

        return list(self.options.keys())[self.current_option]

    def print_details(self):
        character_sheet = self.make_sheet(self.character)
        enemy_sheet = self.make_sheet(self.enemy)

        columns = Columns(
            [
                Panel(character_sheet, title=self.character.name),
                Panel(enemy_sheet, title=self.enemy.name),
            ],
            width=30,
        )

        self.console.print(
            Panel(Text("Battle", justify="center"), width=62), justify="center"
        )
        self.console.print(columns, justify="center")
        self.console.print(
            Panel(
                "".join(self.battle_log[-6:]), title="Battle Log", width=62, height=8
            ),
            justify="center",
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

    def resolve_battle(self, game_state, console):
        battle_finished = False
        enemy_won_roll = self.roll_initiative()
        turn = 0

        while battle_finished is False:
            os.system("clear")
            turn = turn + 1
            self.print_details()
            self.print_options()
            choice = self.choice()
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
                self.print_details()
                console.print(
                    "[bold yellow]\n You won the battle! Your enemy "
                    "lays dead before you...",
                    justify="center",
                )
                time.sleep(3)
                battle_finished = True
            elif self.character.hp <= 0:
                os.system("clear")
                self.print_details()
                console.print(
                    "[bold red]\n Even with all your might, this enemy "
                    "proved too powerful for you.\n Your adventure "
                    "ends here...",
                    justify="center",
                )
                time.sleep(3)
                battle_finished = True
                game_state.game_over = True


def get_active_window_title():
    root = subprocess.Popen(
        ["xprop", "-root", "_NET_ACTIVE_WINDOW"], stdout=subprocess.PIPE
    )
    stdout, stderr = root.communicate()

    m = re.search(b"^_NET_ACTIVE_WINDOW.* ([\\w]+)$", stdout)
    if m is not None:
        window_id = m.group(1)
        window = subprocess.Popen(
            ["xprop", "-id", window_id, "WM_NAME"], stdout=subprocess.PIPE
        )
        stdout, stderr = window.communicate()
    else:
        return None

    match = re.match(b"WM_NAME\\(\\w+\\) = (?P<name>.+)$", stdout)
    if match is not None:
        return match.group("name").strip(b'"')

    return None


def game_menu(game_state, console, game_window):
    text = Text(
        "After a very tiring adventure, you finnaly find a place to rest",
        justify="center",
    )
    options = {
        "save": "Save current adventure and exit",
        "exit": "Exit without saving",
        "return": "Return to your adventure",
    }

    game_menu = Menu(text, options, console, game_window)
    game_menu.print_menu()
    choice = game_menu.choice()

    if choice == "save":
        sav.save_game(game_state, console)
        sys.exit()
    elif choice == "exit":
        sys.exit()


def initialize_game(game_state, console, game_window):

    text = (
        "[bold red]Welcome, adventurer! Are you ready for your next challenge?\n"
        "The world out there is full of monsters and treasures, and\n"
        "they are both waiting for you!\n"
        "Remember: Your choices always matter, so choose wisely."
    )

    options = {
        "create": "Create a character",
        "start": "Start an adventure",
        "load": "Load a saved game",
        "exit": "Exit",
    }

    os.system("clear")

    starting_menu = Menu(text, options, console, game_window)
    starting_menu.print_menu()
    starting_menu.print_options()
    choice = starting_menu.choice()

    if choice == "create":
        os.system("clear")
        cha.create_character(save_folder="Characters/")
        initialize_game(game_state, console, game_window)
    elif choice == "start":
        character_list = [
            f.split(".")[0] for f in os.listdir("Characters") if f.endswith("json")
        ]
        if len(character_list) > 0:
            cha.choose_character(game_state, console, character_list, game_window)
            console.print("\n")
            adv.choose_adventure(game_state, console, game_window)
        elif len(character_list) == 0:
            console.print(
                " Looks like you have not created any characters yet,"
                " try doing that first"
            )
            time.sleep(2)
            initialize_game(game_state, console, game_window)

    elif choice == "load":
        save_list = [f.split(".")[0] for f in os.listdir("Saves") if f.endswith("sav")]
        if len(save_list) > 0:
            game_state = sav.choose_save(game_state, console, save_list)
        elif len(save_list) == 0:
            console.print(" Looks like you don't have any saved files...")
            time.sleep(2)
            initialize_game(game_state, console, game_window)
    elif choice == "exit":
        console.print("Very well, see you next time, adventurer!")
        time.sleep(2)
        sys.exit()


def main_game():
    sys.stdout.write("\x1b[8;30;80t")
    console = Console(width=80, height=30)
    game_window = get_active_window_title()
    gs = GameState()

    initialize_game(gs, console, game_window)
    exit_game = False
    while exit_game is False:
        gs.adventure[gs.next_encounter].resolve_encounter(gs)


if __name__ == "__main__":
    main_game()
