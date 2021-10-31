#!/usr/bin/env python3

import os


def read_adventure(adventure_file):
    import TRPG

    f = open(("Adventures/" + adventure_file + ".txt"), mode="r")
    lines = f.readlines()
    lines = "".join(lines)
    lines = lines.split("*encounter*:")[1:]

    encounters = {}

    for encounter_index in range(len(lines)):
        encounter_raw = lines[encounter_index]

        encounter_name = encounter_raw.split("\n")[0]
        encounter_name = encounter_name.rstrip(" ").lstrip(" ")

        encounter_raw = "\n".join(encounter_raw.split("\n")[1:])

        encounter_description = encounter_raw.split("*options*")[0]
        encounter_description = encounter_description.rstrip("\n ")
        encounter_description = encounter_description.lstrip("\n ")

        encounter_options = encounter_raw.split("*options*")[1]
        encounter_options = encounter_options.rstrip("\n ")
        encounter_options = encounter_options.lstrip("\n ")
        encounter_options = encounter_options.split("*option*\n")[1:]

        options = []
        results = []

        for option_index in range(len(encounter_options)):
            option_raw = encounter_options[option_index]
            option = option_raw.split("*results*\n")[0]
            option = option.rstrip("\n ")
            option = option.lstrip("\n ")

            options.append(option)

            option_results = option_raw.split("*results*\n")[1]
            option_results = option_results.split("\n")
            try:
                option_results.remove("")
            except ValueError:
                option_results = option_results

            results.append(option_results)

        options = dict(enumerate(options))
        results = dict(enumerate(results))

        encounters[encounter_name] = TRPG.Encounter(
            encounter_name, encounter_description, options, results
        )

    f.close()
    return encounters


if __name__ == "__main__":
    os.chdir("..")
    test = read_adventure("test")
