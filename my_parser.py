#!/usr/bin/env python3

import argparse
import engine.keycodes
import json
import yaml
from engine.parser import buttery_parser
from engine.kaleidoscope_parser import buttery_kaleidoscope_parser

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description = "Parse Buttery Engine JSON definition to a QMK compatible keymap"
    )
    parser.add_argument(
        "input",
        metavar = "input",
        type = str,
        help = "Path to the input JSON"
    )
    args = parser.parse_args()

    with open(args.input, "r") as file:
        try:
            keymap_def = json.load(file)
        except json.JSONDecodeError:
            file.seek(0)
            keymap_def = yaml.safe_load(file)

    result = buttery_kaleidoscope_parser(keymap_def)

    with open('engine/kaleidoscope_template.txt', 'r') as file:
        template = file.read()

    keymap = template.format(
        includes = result["includes"],
        keycodes = result["keycodes"],
        pseudolayers = result["pseudolayers"],
        keyboard_parameters = result["keyboard_parameters"],
        keymaps = result["keymaps"],
        buffers = result["buffers"],
        chords = result["chords"],
        leader_sequences = result["leader_sequences"]
    )

    with open('keymap.ino', 'w') as file:
        file.write(keymap)
