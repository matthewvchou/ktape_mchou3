#!/usr/bin/env python3

import sys
import time
import csv

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
    def __init__(self, name: str, num_tapes: int, tape: str, Q: str, start: str, accept: str):
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
        self.tapes = [char for char in tape] + [['_'] for _ in range(num_tapes - 1)]    # Tapes (First contains initial input, rest initalize as blank)
        self.heads = [0 for _ in range(num_tapes)]                                      # Tape Head Positions (All initialized to 0)
        
        # Formal Definition
        # 7-tuple version {Q, SIGMA, GAMMA, sigma, q0, qaccept, qreject}
        self.Q = set(Q.split(','))                                                      # Set of States
        self.input_alphabet = set(char for tape in self.tapes for char in tape)         # Input Alphabet (Not Containing Blank Symbol _)
        if '*' not in self.input_alphabet:
            self.input_alphabet.add('*')
        self.tape_alphabet = self.input_alphabet.union({'_'})                           # Tape Alphabet (Containing Blank Symbol _)
        self.transitions = {}                                                           # Transitions (Will Get in Separate Function)
        self.start = start
        self.accept = accept.split(',')                                                 # Accept States (Assume All Other States are Reject States)
    
    def _make_transitions(self, ):
        print("test")
    
    # def _move(tape_num: int, move: str):

    def _print(self):
        print(f"Name: {self.name}")
        print(f"Number of Tapes: {self.num_tapes}")
        print(f"List of Tapes: {self.tapes}")
        print(f"Head Positions: {self.heads}")
        print(f"Set of States: {self.Q}")
        print(f"Input Alphabet: {self.input_alphabet}")
        print(f"Tape Alphabet: {self.tape_alphabet}")
        print(f"Starting State: {self.start}")
        print(f"Acceptint States: {self.accept}")


def main():
    test = ktape('test', 3, 'ababababaababa', 'q0,q1,q2,q3,q4', 'q0', 'qaccept')
    test._print()

    # Check if a filenames are passed as argument
    if len(sys.argv) < 3:
        print("Usage: python3 knapsack_solver_mchou3.py <input.csv> <output.csv>")
        sys.exit(1)

    # Read in CSV file and initialize TARGET and COINS for each line
    filename = sys.argv[1]

if __name__ == '__main__':
    main()