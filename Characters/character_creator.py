#!/usr/bin/env python3

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
        attributes = []
        for index in range(0, 4):
            print(
                "Let's roll some dice and find out "
                + name
                + "'s attributes"
                + "." * index,
                end="\r",
            )
            attributes.append(random.randint(3, 10))
            time.sleep(0.5)

        attributes.append(attributes[0] * 10)
        attributes.append(max(attributes[0:2]) + 5)

        print("\nYour adventurer is ready! Their attributes are (from 3 to 10):")
        print("- Stength: " + str(attributes[0]))
        print("- Agility: " + str(attributes[1]))
        print("- Intelligence: " + str(attributes[2]))
        print("- Charisma: " + str(attributes[3]) + "\n")
        print("- HP (Strength * 10): " + str(attributes[4]))
        print("- Defense (max(str/agi) + 5): " + str(attributes[5]) + "\n")

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

            f = open((save_folder + name + ".txt"), mode="w")
            for attribute in attributes:
                f.write(str(attribute) + "\n")
            f.close

            time.sleep(3.0)
            attributes_accepted = True
        elif choice == "yes":
            roll = roll + 1
        else:
            print("That's not a valid choice, try again...")
            time.sleep(2)


if __name__ == "__main__":
    create_character()
