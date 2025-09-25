from blessed import Terminal
from collections import deque
from time import sleep
import random

# Configuration constants
BAR_LENGTH_DIVISOR = 1.5
MAX_GAP = 30
MIN_BAR_LENGTH = 1
MIN_GAP = 1
FRAMES_PER_SECOND = 24
COLUMN_SPACING = 2
TERMINAL_TOP_ROW = 0
TERMINAL_LEFT_COLUMN = 0
FIRST_ELEMENT_INDEX = 0
POSITION_OFFSET = 1
LIST_OFFSET = 1

# ANSI color codes
GREEN_COLOR_CODE = '\x1b[32m'
RESET_COLOR_CODE = '\x1b(B\x1b[m'

# Character definitions

sanskrit = ['ख', 'ग', 'घ', 'ङ', 'च', 'छ', 'ज', 'झ', 'ञ', 'ट', 'ठ',
            'ड', 'ढ', 'ण', 'त', 'थ', 'द', 'ध', 'न', 'प', 'फ', 'ब', 'भ', 'म']
english = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
           'm', 'n', 'o', 'p', 'q', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
greek = ['α', 'β', 'γ', 'δ', 'ε', 'ζ', 'η', 'θ', 'ι', 'κ', 'λ',
         'μ', 'ν', 'ξ', 'ο', 'π', 'ρ', 'σ', 'τ', 'υ', 'φ', 'χ', 'ψ', 'ω']
kannada = ['ಅ', 'ಆ', 'ಇ', 'ಈ', 'ಎ', 'ಏ', 'ಐ', 'ಒ',
           'ಓ', 'ಔ', 'ಕ', 'ಖ', 'ಗ', 'ಘ', 'ಙ', 'ಚ', 'ಛ', 'ಜ']


languages = english + kannada + sanskrit + greek + numbers


class Bar(object):

    def __init__(self, t, x):
        self.length = random.randint(MIN_BAR_LENGTH, int(t.height//BAR_LENGTH_DIVISOR))
        self.gap = random.randint(MIN_GAP, MAX_GAP)
        self.pos = TERMINAL_TOP_ROW
        self.t = t
        self.languages = languages
        self.x = x
        self.has_u_neighbour = False  # upstairs neighbour

    def extend(self, scene):

        def go_green(x):
            return GREEN_COLOR_CODE + x + RESET_COLOR_CODE if self.t.green not in x else x

        if self.has_gone():
            return

        if self.pos < self.length:
            scene[self.pos - POSITION_OFFSET][self.x] = go_green(scene[self.pos - POSITION_OFFSET][self.x])
            scene[self.pos][self.x] = random.choice(self.languages)
        else:
            if self.pos < self.t.height:
                scene[self.pos - POSITION_OFFSET][self.x] = go_green(scene[self.pos - POSITION_OFFSET][self.x])
                scene[self.pos][self.x] = random.choice(self.languages)
            if self.pos - self.length < self.t.height:
                scene[self.pos - self.length][self.x] = ' '
        self.pos += POSITION_OFFSET

    def has_gone(self):
        return self.pos >= self.t.height + self.length

    def has_fully_extended(self):
        return self.pos >= self.length + self.gap


def print_term(t, matrix):
    with t.location(TERMINAL_TOP_ROW, TERMINAL_LEFT_COLUMN):
        print('\n'.join([''.join(row) for row in matrix]), end='\r')

def init_matrix(t):
    return [[' ' for x in range(t.width)] for y in range(t.height)]

def init_columns(t):
    return [deque([Bar(t, idx)]) if idx % COLUMN_SPACING == TERMINAL_TOP_ROW else None
            for idx in range(t.width)]

def matrix_rain(t):
    matrix = init_matrix(t)
    columns = init_columns(t)

    with t.hidden_cursor():
        while True:
            if len(matrix) != t.height or len(matrix[FIRST_ELEMENT_INDEX]) != t.width:
                matrix = init_matrix(t)
                columns = init_columns(t)
            for _q in columns:
                if not _q:
                    continue
                new_bars = []
                for b in _q:
                    b.extend(matrix)
                    if b.has_fully_extended() and not b.has_u_neighbour:
                        new_bars.append(Bar(t, b.x))
                        b.has_u_neighbour = True
                _q.extend(new_bars)
                if _q[FIRST_ELEMENT_INDEX].has_gone():
                    _q.popleft()
            print_term(t, matrix)
            sleep(1/FRAMES_PER_SECOND)


def main():
    t = Terminal()
    while True:
        try:
            matrix_rain(t)
        except KeyboardInterrupt:
            print(t.clear())
            break


if __name__ == '__main__':
    main()
