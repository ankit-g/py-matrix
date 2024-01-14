from pyneorain import Bar
from blessed import Terminal
from collections import deque
import signal
from multiprocessing import Process
from time import sleep


def print_term(t, matrix):
    with t.location(0, 0):
        print('\n'.join([''.join(row[:t.width]) for row in matrix[:t.height]]), end='\r')

def init_matrix(t):
    return [[' ' for x in range(t.width)] for y in range(t.height)]

def init_columns(t):
    return [deque([Bar(t, idx)]) if idx%2 else None
            for idx in range(t.width)]

def matrix_rain(t):
    matrix = init_matrix(t)
    columns = init_columns(t)

    with t.hidden_cursor():
        while True:
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
                if _q[0].has_gone():
                    _q.popleft()
            print_term(t, matrix)
            sleep(1/24)


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
