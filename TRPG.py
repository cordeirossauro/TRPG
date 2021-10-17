#!/usr/bin/env python3

import os
import time
import sys
import random

class Encounter:
    
    def __init__(self, Name, Description, Options):
        self.Name = Name
        self.Description = Description
        self.Options = Options
        
class Character:
    
    def __init__(self, Name, Strength, Agility, Intelligence, Charisma):
        self.Name = Name
        self.Strength = Strength
        self.Agility = Agility
        self.Intelligence = Intelligence
        self.Charisma = Charisma
        
        
def ReadAdventure(AdventureFile):
    f = open(('Adventures/' + AdventureFile), mode = 'r')
    Lines = f.readlines()
    Encounters = []
    
    CurrentLineNumber = 0
    TotalEncounters = 0
    AdventureFinished = False
    while AdventureFinished == False:
        Line = Lines[CurrentLineNumber]
        if Line.split(':')[0] == '*encounter*':
            Name = Line.split(':')[1].rstrip('\n')
            Description = ''
            DescriptionFinished = False
            while DescriptionFinished == False:
                CurrentLineNumber = CurrentLineNumber + 1
                Line = Lines[CurrentLineNumber]
                if Line != '*options*\n':
                    Description = Description + Line
                else:
                    DescriptionFinished = True
                
            Options = {}
            OptionsFinished = False
            while OptionsFinished == False:
                CurrentLineNumber = CurrentLineNumber + 1
                Line = Lines[CurrentLineNumber]
                if (Line != '*end*\n') & (Line != '*end*'):
                    OptionNumber = Line.split('.')[0]
                    Option = Line.split('.')[1]
                    Options[OptionNumber] = Option
                else:
                    OptionsFinished = True
            
            Encounters.append(Encounter(Name, Description, Options))
            TotalEncounters = TotalEncounters + 1
            
        CurrentLineNumber = CurrentLineNumber + 1
        if CurrentLineNumber >= len(Lines):
            AdventureFinished = True
                
    f.close()
    return Encounters


def ChooseAdventure():
    AdventureList = os.listdir('Adventures')
    print('\nChoose your adventure:')
    Index = 0
    
    for Adventure in AdventureList:
        Index = Index + 1
        print(str(Index) + '. ' + Adventure)
    
    Index = Index + 1
    print(str(Index) + '. Return')
    
    ChoiceReceived = False
    while ChoiceReceived == False:
        Choice = int(input('Your choice (number): '))
        if (Choice > 0) & (Choice < Index):
            Adventure = ReadAdventure(AdventureList[Choice - 1])
            ChoiceReceived = True
        elif Choice == Index:
            Adventure = 0
            ChoiceReceived = True
        else:
            print('That\'s not a valid choice, try again...')
            time.sleep(2)
            
    return Adventure


def CreateCharacter(Rolls = 3):
    print('Welcome to the character creator! First things first, what\'s your hero\'s name?')
    Name = input()
    
    AttributesAccepted = False
    Roll = 1
    
    while (AttributesAccepted == False) & (Roll <= Rolls):
        Attributes = []
        for Index in range(0, 4):
            print('Let\'s roll some dice and find out ' + Name + '\'s attributes' + '.' * Index, end = '\r')
            Attributes.append(random.randint(3, 10))
            time.sleep(0.5)
        
        print('\nYour adventurer is ready! Their attributes are (from 3 to 10):')
        print('- Strength: ' + str(Attributes[0]))
        print('- Agility: ' + str(Attributes[1]))
        print('- Intelligence: ' + str(Attributes[2]))
        print('- Charisma: ' + str(Attributes[3]) + '\n')
        
        if Roll < Rolls:
            Choice = input('Would you like to roll again? You have ' + str(Rolls - Roll) + ' more chance(s) (yes/no) \n').lower()
        elif Roll == Rolls:
            print('You\'re out of chances')
            Choice = 'no'
        
        if Choice == 'no':
            print('Very well, your character was created!')
            print('Returning to the starting menu...')
            
            f = open(('Characters/' + Name + '.txt'), mode = 'w')
            for Attribute in Attributes:
                f.write(str(Attribute) + '\n')
            f.close
            
            time.sleep(3.0)
            AttributesAccepted = True
        elif Choice == 'yes':
            Roll = Roll + 1
        else:
            print('That\'s not a valid choice, try again...')
            time.sleep(2)
            
   
def ReadCharacter(Name):
    f = open(('Characters/' + Name), mode = 'r')
    Attributes = []
    for Attribute in f.readlines():
        Attributes.append(int(Attribute))
   
    Hero = Character(Name.split('.')[0], Attributes[0], Attributes[1], Attributes[2], Attributes[3])
    
    return Hero
   
    
def ChooseCharacter():
    CharacterList = os.listdir('Characters')
    os.system('clear')
    print('Choose your character:')
    Index = 0
    
    for Character in CharacterList:
        Index = Index + 1
        print(str(Index) + '. ' + Character.split('.')[0])
        
    Index = Index + 1
    print(str(Index) + '. Return')
    
    ChoiceReceived = False
    while ChoiceReceived == False:
        Choice = int(input('Your choice (number): '))
        if (Choice > 0) & (Choice < Index):
            Character = ReadCharacter(CharacterList[Choice - 1])
            ChoiceReceived = True
        elif Choice == Index:
            Character = 0
            ChoiceReceived = True
        else:
            print('That\'s not a valid choice, try again...')
            time.sleep(2)
            
    return Character


def PrintOptions(Options):
    for Option in Options:
        print(Options[Option])


def StartingMenu():
    Options = {'create': '- Create a character',
               'start': '- Start an adventure',
               'exit': '- Exit'
                }
    
    ChoiceMade = False
    while ChoiceMade == False:
        os.system('clear')
        print('Welcome, adventurer! Are you ready for your next challenge?')
        print('The world out there is full of monsters and treasures, and '\
              'they are both waiting for you!')
        print('Remember: Your choices always matter, so choose wisely.')
        PrintOptions(Options)
        
        Choice = input('What would you like to do? (create/start/exit)\n')
        if Choice == 'create':
            os.system('clear')
            CreateCharacter()
        elif Choice == 'start':
            if len(os.listdir('Characters')) > 0:
                Character = ChooseCharacter()
                if Character != 0:
                    Adventure = ChooseAdventure()
                    if Adventure != 0:
                        ChoiceMade = True
            elif len(os.listdir('Characters')) == 0:
                print('Looks like you have not created any characters yet, try doing that first')
                time.sleep(2)
        elif Choice == 'exit':
            print('Very well, see you next time, adventurer!')
            time.sleep(2)
            sys.exit()
        else:
            print('That\'s not a valid choice, try again...')
            time.sleep(2)
            
            
    return Character, Adventure
            

Character, Adventure = StartingMenu()