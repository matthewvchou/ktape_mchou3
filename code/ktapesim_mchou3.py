#!/usr/bin/env python3

import sys
import time
import csv
from itertools import product

'''

Matthew Chou - mchou3
December 8th, 2024
Theory of Computing Project 02

ktapesim_mchou3.py: k-tape machine simulator

'''

# Constants
TAPE_MOVEMENTS = {  'L': -1,
                    'R': 1, 
                    'S': 0}

# ktape Machine Class

class ktape:
    def __init__(self, name: str, num_tapes: int, tape: str, Q: list[str], start: str, accept: list[str]):
        '''
        Initialization of ktape Object.

        Input:
            name:           Name of k-tape Machine
            num_tapes:      k = Number of Tapes in Machine
            tape:           Input Tape/First Tape - All Other Tapes Start Empty
            Q:              Set of All States
            start:          Starting State
            accept:         Set of All Accept States (Rest of States Considered Reject States)
        '''
        # k-Tape Machine Metadata
        self.name = name                                                                # Tape Name
        self.num_tapes = num_tapes                                                      # Number of Tapes (k)
        self.tapes = [[char for char in tape]] + [['_'] for _ in range(num_tapes - 1)]  # Tapes (First contains initial input, rest initalize as blank)
        self.heads = [0 for _ in range(num_tapes)]                                      # Tape Head Positions (All initialized to 0)
        self.current_state = start                                                      # Current State
        
        # Formal Definition
        # 7-tuple version {Q, SIGMA, GAMMA, sigma, q0, qaccept, qreject}
        self.Q = set(Q)                                                                 # Set of States
        self.input_alphabet = set(char for tape in self.tapes for char in tape)         # Input Alphabet (Not Containing Blank Symbol _)
        if '*' not in self.input_alphabet:
            self.input_alphabet.add('*')
        self.tape_alphabet = self.input_alphabet.union({'_'})                           # Tape Alphabet (Containing Blank Symbol _)
        self.transitions = {}                                                           # Transitions (Will Get in Separate Function)
        self.start = start                                                              # Starting State
        self.accept = accept                                                            # Accept States (Assume All Other States are Reject States)

    def _simulate(self):
        print(f"Machine Name: {self.name}")
        print(f"Input String: {''.join(self.tapes[0])}")

    def _replace_wildcards(self, tape_list):
        # Create new tape lists with characters in tape alphabet applied to all wildcards
        for char in self.tape_alphabet:
            if char == '*':
                continue
            new_tape = [char if value == '*' else value for value in tape_list]
            yield new_tape

    def _make_transition(self, raw: list[str]):
        # Look to see if wildcard appears
        if '*' in raw:
            for replacement in self._replace_wildcards(raw):
                self._make_transition(replacement)
        else:
            # Splicing the list into appropriate tuples for dictionary entry
            self.transitions[(raw[0], tuple(raw[1:self.num_tapes + 1]))] = (raw[self.num_tapes + 1], tuple(raw[self.num_tapes + 2:self.num_tapes * 2 + 2]), tuple(raw[self.num_tapes * 2 + 2:]))

# Main
def main():
    # Check if a filenames are passed as argument
    if len(sys.argv) < 2:
        print("Usage: python3 ktapesim_mchou3.py <full path to input.csv>")
        sys.exit(1)

    # Read in CSV file and initialize k-tape machine
    filename = sys.argv[1]
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        # First 5 rows: Machine Name, Number of Tapes, Tape Input, Set of States, Starting State, Accepting States
        first_five = [next(reader) for _ in range(5)]
        machine = ktape(first_five[0][0], int(first_five[0][1]), first_five[1][0], first_five[2], first_five[3][0], first_five[4])
        # For the rest of the rows in CSV file, should be 
        for raw in reader:
            machine._make_transition(raw)
        machine._simulate()

if __name__ == '__main__':
    main()