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

    def _replace_wildcards(self, tape_list):
        '''
        Replaces wildcards within transition.

        Input:
            tape_list:  Instance of transition with wildcards in it.
        
        Output:
            new_tape:   Instance of transition with wildcards replaced with characters in tape alphabet (yields one instance per character in tape alphabet minus the '*' character)
        '''
        # Create new tape lists with characters in tape alphabet applied to all wildcards
        for char in self.tape_alphabet:
            # Skipping the '*' character
            if char == '*':
                continue
            # Replace '*' character with new character
            new_transition = [char if value == '*' else value for value in tape_list]
            # Yield new transition
            yield new_transition

    def _make_transition(self, raw: list[str]):
        '''
        Making a singluar instance of a transition.

        Input:
            raw:  Instance of a transition in a raw for (list of strings).
        '''
        # See if wildcard appears within the transition
        if '*' in raw:
            # If it does, then create a new transition for each other character within the tape alphabet
            for replacement in self._replace_wildcards(raw):
                self._make_transition(replacement)
        # Creating a new transition
        else:
            # Splicing the list into appropriate tuples for dictionary entry
            self.transitions[(raw[0], tuple(raw[1:self.num_tapes + 1]))] = (raw[self.num_tapes + 1], tuple(raw[self.num_tapes + 2:self.num_tapes * 2 + 2]), tuple(raw[self.num_tapes * 2 + 2:]))

    def _take_transition(self, step: int):
        '''
        Simulating a SINGULAR transition based on the current state of the machine and the characters of the tape heads.

        Input:
            step:  The current iteration/transition number the machine is on.
        '''
        # Creating tuple of the characters the each respective tape head is pointing to
        reading = tuple(self.tapes[i][position] for i, position in enumerate(self.heads))
        # Creating tuple of the full transition
        current = (self.current_state, reading)

        # Attempting to take a transition
        try:
            transition = self.transitions[current]
        # If the transition is not found, then stop the machine --> Means that the machine will not accept the string
        except:
            print("------------------")
            print(f"Transition {current} does not exist.")
            print("String is NOT accepted.")
            sys.exit(1)

        # Getting the machine state after the transition is taken
        next_state = transition[0]
        writing = transition[1]
        movements = transition[2]

        # Print status of machine after the transition is taken
        print("------------------")
        print(f"Step {step}")
        print(f"Next State: {next_state}")
        # Taking actual transition
        self._write_and_move(writing, movements)
        # For each tape, print out the status of the tape after taking the transition
        for tape_number in range(self.num_tapes):
            print(f"Tape {tape_number}: {' '.join(self.tapes[tape_number])}")
            pointer_line = ' '.join('^' if i == self.heads[tape_number] else ' ' for i in range(len(self.tapes[tape_number])))
            print(f"        {pointer_line}")

        # Update the current state of the machine
        self.current_state = next_state

    def _write_and_move(self, writing, movements):
        '''
        Writing characters to the tape and also moving tape heads for all tapes per transition.

        Input:
            writing:    What the should be written to each tape.
            movements:  How each tape head should move.
        '''
        # Go through all tapes and write/move respectively
        for tape_number in range(self.num_tapes):
            # Write the character onto the tape
            self.tapes[tape_number][self.heads[tape_number]] = writing[tape_number]
            # Move the tape head
            self.heads[tape_number] += TAPE_MOVEMENTS[movements[tape_number]]
            # SPECIAL CASE: If the tape has reached the 'end' (i.e. no more unique characters), then append on a blank character
            if self.heads[tape_number] >= len(self.tapes[tape_number]):
                self.tapes[tape_number].append('_')
            # SPECIAL CASE: If the tape head attempts to go left past the first element, add a blank to the beginning of the tape and set head to 0
            # This gives the tape the infinite-ness on BOTH ends
            if self.heads[tape_number] < 0:
                self.tapes[tape_number].insert(0, '_')
                self.heads[tape_number] = 0


    def _simulate(self):
        '''
        Simulates the entire ktape machine, taking whichever transition possible.
        '''
        # Print Machine Name, Input String, and Starting State
        print(f"Machine Name: {self.name}")
        input_string = ''.join(self.tapes[0])
        print(f"Input String: {input_string}")
        print(f"Start State : {self.start}")
        step = 1

        # Taking Whichever Transition Possible
        # NOTE: We are assuming that the first tape is the 'control' tape and will properly stop when a blank is reached
        while(self.tapes[0][self.heads[0]] != '_'):
            self._take_transition(step)
            step += 1
        # Take one more transition --> necessary to reach accept state
        self._take_transition(step)
        # Print if string was accepted or not
        print("------------------")
        if self.current_state in self.accept:
            print(f"{input_string} is Accepted.")
        else:
            print(f"{input_string} is NOT Accepted.")


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
        # For the rest of the rows in CSV file, should be transitions --> Add in transitions
        for raw in reader:
            machine._make_transition(raw)
        # Simulate the entirety of the ktape machine
        machine._simulate()

if __name__ == '__main__':
    main()