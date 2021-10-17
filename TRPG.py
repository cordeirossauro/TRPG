#!/usr/bin/env python3

import os
import time
import sys
import random

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
    print('\nChoose your adventure:')
    index = 0
    
    for adventure in adventure_list:
        index = index + 1
        print(str(index) + '. ' + adventure)
    
    index = index + 1
    print(str(index) + '. Return')
    
    choice_received = False
    while choice_received == False:
        choice = int(input('Your choice (number): '))
        if (choice > 0) & (choice < index):
            adventure = read_adventure(adventure_list[choice - 1])
            choice_received = True
        elif choice == index:
            adventure = 0
            choice_received = True
        else:
            print('That\'s not a valid choice, try again...')
            time.sleep(2)
            
    return adventure


def create_character(rolls = 3):
    print('Welcome to the character creator! First things first, what\'s your hero\'s name?')
    name = input()
    
    attributes_accepted = False
    roll = 1
    
    while (attributes_accepted == False) & (roll <= rolls):
        attributes = []
        for index in range(0, 4):
            print('Let\'s roll some dice and find out ' + name + '\'s attributes' + '.' * index, end = '\r')
            attributes.append(random.randint(3, 10))
            time.sleep(0.5)
        
        print('\nYour adventurer is ready! Their attributes are (from 3 to 10):')
        print('- Stength: ' + str(attributes[0]))
        print('- Agility: ' + str(attributes[1]))
        print('- Intelligence: ' + str(attributes[2]))
        print('- Charisma: ' + str(attributes[3]) + '\n')
        
        if roll < rolls:
            choice = input('Would you like to roll again? You have ' + str(rolls - roll) + ' more chance(s) (yes/no) \n').lower()
        elif roll == rolls:
            print('You\'re out of chances')
            choice = 'no'
        
        if choice == 'no':
            print('Very well, your character was created!')
            print('Returning to the starting menu...')
            
            f = open(('Characters/' + name + '.txt'), mode = 'w')
            for attribute in attributes:
                f.write(str(attribute) + '\n')
            f.close
            
            time.sleep(3.0)
            attributes_accepted = True
        elif choice == 'yes':
            roll = roll + 1
        else:
            print('That\'s not a valid choice, try again...')
            time.sleep(2)
            
   
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
    print('Choose your character:')
    index = 0
    
    for character in character_list:
        index = index + 1
        print(str(index) + '. ' + character.split('.')[0])
        
    index = index + 1
    print(str(index) + '. Return')
    
    choice_received = False
    while choice_received == False:
        choice = int(input('Your choice (number): '))
        if (choice > 0) & (choice < index):
            character = read_character(character_list[choice - 1])
            choice_received = True
        elif choice == index:
            character = 0
            choice_received = True
        else:
            print('That\'s not a valid choice, try again...')
            time.sleep(2)
            
    return character


def print_options(options):
    for option in options:
        print(options[option].split(':')[0])


def starting_menu():
    options = {'create': '- Create a character',
               'start': '- Start an adventure',
               'exit': '- Exit'
                }
    
    choice_made = False
    while choice_made == False:
        os.system('clear')
        print('Welcome, adventurer! Are you ready for your next challenge?')
        print('The world out there is full of monsters and treasures, and '\
              'they are both waiting for you!')
        print('Remember: Your choices always matter, so choose wisely.')
        print_options(options)
        
        choice = input('What would you like to do? (create/start/exit)\n')
        if choice == 'create':
            os.system('clear')
            create_character()
        elif choice == 'start':
            if len(os.listdir('Characters')) > 0:
                character = choose_character()
                if character != 0:
                    adventure = choose_adventure()
                    if adventure != 0:
                        choice_made = True
            elif len(os.listdir('Characters')) == 0:
                print('Looks like you have not created any characters yet, try doing that first')
                time.sleep(2)
        elif choice == 'exit':
            print('Very well, see you next time, adventurer!')
            time.sleep(2)
            sys.exit()
        else:
            print('That\'s not a valid choice, try again...')
            time.sleep(2)
            
    return character, adventure
            

def resolve_encounter(encounter):
    os.system('clear')
    print(encounter.description)
    print_options(encounter.options)
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
    character, adventure = starting_menu()
    exit_game = False
    current_encounter = 'first_encounter'
    while exit_game == False:
        current_encounter = resolve_encounter(adventure[current_encounter])
        
        
main_game()