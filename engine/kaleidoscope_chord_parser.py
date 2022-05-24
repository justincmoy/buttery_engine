from engine.utils import plus_separator, newline_separator, comma_separator, my_format, unpack_by_chars
from engine.kaleidoscope_keycodes import expand_keycode
from functools import reduce

chords = []
chord_keys_output = []
strings = []

simple_chord = """[{index}] = {{
        .action = simple_chord,
        .keys = {{{keycodes}}}
    }}
"""

def add_simple_chord(pseudolayer, original_keycode, chord_keys):
    global chords
    global chord_keys_output
    global strings
    
    keycode = expand_keycode(original_keycode)

    if keycode.startswith("Key"):
        chords.append(my_format(s = simple_chord,
             index = len(chords),
             on_pseudolayer = pseudolayer,
             keycodes = reduce(comma_separator, chord_keys)))
        chord_keys_output.append(keycode)
    else:
        print(f"Unrecognized keycode {keycode}")

def add_chord_set_with_keycode(pseudolayer, keycodes):
    for keycode in keycodes:
        add_simple_chord(pseudolayer, keycode["keycode"], keycode["chord"])

def parse_chords(keymap_def):
    global chords
    global chord_keys_output
    global strings

    for pseudolayer in keymap_def["pseudolayers"]:
        for chord in pseudolayer["chords"]:
            if chord["type"] == "chord_set_with_keycode":
                add_chord_set_with_keycode(pseudolayer["name"], chord["keycodes"])
            else:
                raise Exception(f"Unrecognized chord type {chord['type']}")

    return f"""
USE_MAGIC_COMBOS({reduce(comma_separator, chords)});

Key chord_keys[{len(chord_keys_output)}] = {{{reduce(comma_separator, chord_keys_output)}}};
"""
