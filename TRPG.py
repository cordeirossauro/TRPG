#!/usr/bin/env python3

import os
import time
import sys
import random

os.chdir("Characters")
import character_creator as cc
os.chdir("..")

class Menu:
    
    def __init__(self, text, options):
        self.text = text
        self.options = options
        
    def print_menu(self, numbered_choices = False):
        print(self.text)
        for option in self.options:
            if numbered_choices == True:
                print(str(int(option) + 1) + '. ' + self.options[option].split(':')[0])
            else:
                print('- ' + self.options[option].split(':')[0])
            
    def choice(self, numbered_choices = False):
        
        if numbered_choices == True:
            print('What would you like to do? (Choose a number)')
        else:
            joined_options = '('
            for option in self.options:
                joined_options = joined_options + '/' + option
            joined_options = joined_options + ')'
            joined_options = joined_options.replace('(/', '(')
            print('What would you like to do? ' + joined_options)
            
        choice_received = False
        while choice_received == False:
            
            choice = input('Your choice: ')
            if numbered_choices == True:
                choice = int(choice) - 1
            
            if choice in self.options:
                choice_received = True
            else:
                print('That\'s not a valid choice, try again...')
                time.sleep(2)
        
        return choice
                
    
class Encounter:
    
    def __init__(self, name, description, options):
        self.name = name
        self.description = description
        self.options = options
        
        
class Character:
    
    def __init__(self, name, stength, agility, intelligence, charisma):
        self.name = name
        self.stength = stength
        self.agility = agility
        self.intelligence = intelligence
        self.charisma = charisma
        
        
def read_adventure(adventure_file):
    f = open(('Adventures/' + adventure_file), mode = 'r')
    lines = f.readlines()
    encounters = {}
    
    current_line_number = 0
    adventure_finished = False
    while adventure_finished == False:
        line = lines[current_line_number]
        if line.split(':')[0] == '*encounter*':
            name = line.split(':')[1].strip('\n ')
            description = ''
            description_finished = False
            while description_finished == False:
                current_line_number = current_line_number + 1
                line = lines[current_line_number]
                if line != '*options*\n':
                    description = description + line
                else:
                    description_finished = True
                
            options = {}
            options_finished = False
            while options_finished == False:
                current_line_number = current_line_number + 1
                line = lines[current_line_number]
                if (line != '*end*\n') & (line != '*end*'):
                    option_number = line.split('.')[0]
                    option = line
                    options[option_number] = option
                else:
                    options_finished = True
            
            encounters[name] = Encounter(name, description, options)
            
        current_line_number = current_line_number + 1
        if current_line_number >= len(lines):
            adventure_finished = True
                
    f.close()
    return encounters


def choose_adventure():
    adventure_list = os.listdir('Adventures')
    text = ('\nWhich adventure are you taking today?')
    options = dict(enumerate(adventure_list))
    options[len(adventure_list)] = 'Return'
    
    adventure_menu = Menu(text, options)
    adventure_menu.print_menu(numbered_choices=True)
    choice = adventure_menu.choice(numbered_choices=True)
                          
    if choice == (len(adventure_list)):
        initialize_game()       
    else:
        adventure = read_adventure(adventure_list[choice])
            
    return adventure
            
   
def read_character(name):
    f = open(('Characters/' + name), mode = 'r')
    attributes = []
    for attribute in f.readlines():
        attributes.append(int(attribute))
   
    hero = Character(name.split('.')[0], attributes[0], attributes[1], attributes[2], attributes[3])
    
    return hero
   
    
def choose_character():
    character_list = os.listdir('Characters')
    os.system('clear')
    text = ('Choose your character:')
    options = dict(enumerate(character_list))
    options[len(character_list)] = 'Return'
    
    character_menu = Menu(text, options)
    character_menu.print_menu(numbered_choices=True)
    choice = character_menu.choice(numbered_choices=True)

    if choice == (len(character_list)):
        initialize_game()       
    else:
        character = read_character(character_list[choice])
            
    return character


def initialize_game():
    text = ('Welcome, adventurer! Are you ready for your next challenge?\n'\
            'The world out there is full of monsters and treasures, and '\
            'they are both waiting for you!\n'\
            'Remember: Your choices always matter, so choose wisely.')
    
    options = {'create': 'Create a character',
               'start': 'Start an adventure',
               'exit': 'Exit'
                }
    
    os.system('clear')
    
    starting_menu = Menu(text, options)
    starting_menu.print_menu()
    choice = starting_menu.choice()
    

    if choice == 'create':
        os.system('clear')
        character = cc.create_character(save_folder = 'Characters/')
        initialize_game()
    elif choice == 'start':
        if len(os.listdir('Characters')) > 0:
            character = choose_character()
            adventure = choose_adventure()
        elif len(os.listdir('Characters')) == 0:
            print('Looks like you have not created any characters yet, try doing that first')
            time.sleep(2)
            initialize_game()
    elif choice == 'exit':
        print('Very well, see you next time, adventurer!')
        time.sleep(2)
        sys.exit()
            
    return character, adventure
            

def resolve_encounter(encounter):
    os.system('clear')
    print(encounter.description)
    commands = list(encounter.options.keys())
    
    
    joined_commands = '(' + commands[0]
    for command in commands[1:]:
        joined_commands = joined_commands + '/' + command
    joined_commands = joined_commands + ')'
    
    print('\n What would you like to do? ' + joined_commands)
    choice_received = False
    while choice_received == False:
        choice = input('Your choice (number): ')
        if (choice in commands):
            choice_received = True
        else:
            print('That\'s not a valid choice, try again...')
            time.sleep(2)
    
    next_encounter = encounter.options[choice].split(':')[1].strip('\n ')
    
    return next_encounter

def main_game():
    character, adventure = initialize_game()
    exit_game = False
    current_encounter = 'first_encounter'
    while exit_game == False:
        current_encounter = resolve_encounter(adventure[current_encounter])
        
        
main_game()