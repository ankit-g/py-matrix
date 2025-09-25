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

# ANSI color codes
GREEN_COLOR_CODE = '\x1b[32m'
RESET_COLOR_CODE = '\x1b(B\x1b[m'

# Character definitions
sanskrit = ['ख', 'ग', 'घ', 'ङ', 'च', 'छ', 'ज', 'झ', 'ञ', 'ट', 'ठ',
            'ड', 'ढ', 'ण', 'त', 'थ', 'द', 'ध', 'न', 'प', 'फ', 'ब', 'भ', 'म']
english = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
           'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
greek = ['α', 'β', 'γ', 'δ', 'ε', 'ζ', 'η', 'θ', 'ι', 'κ', 'λ',
         'μ', 'ν', 'ξ', 'ο', 'π', 'ρ', 'σ', 'τ', 'υ', 'φ', 'χ', 'ψ', 'ω']
kannada = ['ಅ', 'ಆ', 'ಇ', 'ಈ', 'ಎ', 'ಏ', 'ಐ', 'ಒ',
           'ಓ', 'ಔ', 'ಕ', 'ಖ', 'ಗ', 'ಘ', 'ಙ', 'ಚ', 'ಛ', 'ಜ']

LANGUAGES = english + kannada + sanskrit + greek + numbers

# Pure functions for bar operations

def create_bar(terminal_height, x):
    """Create a new bar data structure (pure function)."""
    return {
        'length': random.randint(MIN_BAR_LENGTH, int(terminal_height // BAR_LENGTH_DIVISOR)),
        'gap': random.randint(MIN_GAP, MAX_GAP),
        'pos': TERMINAL_TOP_ROW,
        'x': x,
        'has_u_neighbour': False
    }

def make_green(char, terminal):
    """Apply green color to character if not already colored (pure function)."""
    return GREEN_COLOR_CODE + char + RESET_COLOR_CODE if terminal.green not in char else char

def has_bar_gone(bar, terminal_height):
    """Check if bar has moved completely off screen (pure function)."""
    return bar['pos'] >= terminal_height + bar['length']

def has_bar_fully_extended(bar):
    """Check if bar has reached full extension and gap (pure function)."""
    return bar['pos'] >= bar['length'] + bar['gap']

def update_bar_position(bar, scene, terminal):
    """Update bar position and modify scene, returning new bar state (functional)."""
    if has_bar_gone(bar, terminal.height):
        return bar  # No changes needed

    new_bar = bar.copy()  # Create new state instead of modifying

    if bar['pos'] < bar['length']:
        # Bar is still growing
        if bar['pos'] > 0:
            scene[bar['pos'] - POSITION_OFFSET][bar['x']] = make_green(
                scene[bar['pos'] - POSITION_OFFSET][bar['x']], terminal
            )
        scene[bar['pos']][bar['x']] = random.choice(LANGUAGES)
    else:
        # Bar is moving and leaving trail
        if bar['pos'] < terminal.height:
            scene[bar['pos'] - POSITION_OFFSET][bar['x']] = make_green(
                scene[bar['pos'] - POSITION_OFFSET][bar['x']], terminal
            )
            scene[bar['pos']][bar['x']] = random.choice(LANGUAGES)

        # Clear the tail
        tail_pos = bar['pos'] - bar['length']
        if tail_pos >= 0 and tail_pos < terminal.height:
            scene[tail_pos][bar['x']] = ' '

    new_bar['pos'] += POSITION_OFFSET
    return new_bar

def should_spawn_new_bar(bar):
    """Determine if a new bar should be spawned (pure function)."""
    return has_bar_fully_extended(bar) and not bar['has_u_neighbour']

def mark_bar_has_neighbour(bar):
    """Mark bar as having an upstairs neighbour (functional)."""
    new_bar = bar.copy()
    new_bar['has_u_neighbour'] = True
    return new_bar

def update_column_bars(bars, scene, terminal):
    """Update all bars in a column, returning new bar list (functional)."""
    new_bars = []
    bars_to_spawn = []

    for bar in bars:
        updated_bar = update_bar_position(bar, scene, terminal)

        if should_spawn_new_bar(updated_bar):
            bars_to_spawn.append(create_bar(terminal.height, updated_bar['x']))
            updated_bar = mark_bar_has_neighbour(updated_bar)

        if not has_bar_gone(updated_bar, terminal.height):
            new_bars.append(updated_bar)

    return new_bars + bars_to_spawn

def print_scene(terminal, matrix):
    """Print the matrix scene to terminal (pure I/O function)."""
    with terminal.location(TERMINAL_TOP_ROW, TERMINAL_LEFT_COLUMN):
        print('\n'.join([''.join(row) for row in matrix]), end='\r')

def init_matrix(terminal):
    """Initialize empty matrix (pure function)."""
    return [[' ' for x in range(terminal.width)] for y in range(terminal.height)]

def init_columns(terminal):
    """Initialize column structure with initial bars (functional)."""
    columns = []
    for idx in range(terminal.width):
        if idx % COLUMN_SPACING == TERMINAL_TOP_ROW:
            columns.append([create_bar(terminal.height, idx)])
        else:
            columns.append([])
    return columns

def should_reinit_matrix(matrix, terminal):
    """Check if matrix needs reinitialization due to terminal resize (pure function)."""
    return (len(matrix) != terminal.height or
            len(matrix[FIRST_ELEMENT_INDEX]) != terminal.width)

def matrix_rain(terminal):
    """Main matrix rain loop using functional approach."""
    matrix = init_matrix(terminal)
    columns = init_columns(terminal)

    with terminal.hidden_cursor():
        while True:
            if should_reinit_matrix(matrix, terminal):
                matrix = init_matrix(terminal)
                columns = init_columns(terminal)

            # Update all columns functionally
            new_columns = []
            for column_bars in columns:
                if column_bars:
                    new_columns.append(update_column_bars(column_bars, matrix, terminal))
                else:
                    new_columns.append([])

            columns = new_columns
            print_scene(terminal, matrix)
            sleep(1 / FRAMES_PER_SECOND)

def main():
    """Main entry point."""
    terminal = Terminal()
    while True:
        try:
            matrix_rain(terminal)
        except KeyboardInterrupt:
            print(terminal.clear())
            break

if __name__ == '__main__':
    main()
