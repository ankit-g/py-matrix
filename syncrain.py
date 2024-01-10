from pyneorain import Bar
from blessed import Terminal
from collections import deque
import signal
from multiprocessing import Process
from time import sleep

class TerminalResize(Exception):
    pass

def print_term(t, matrix):
    with t.location(0, 0):
        print('\n'.join([''.join(row) for row in matrix]), end='\r')

def matrix_rain():
    t = Terminal()
    matrix = [[' ' for x in range(t.width)] for y in range(t.height)]
    columns = [deque([Bar(t, idx)]) if idx%2 else None 
                for idx in range(t.width)]
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


def handle_sigwinch(signum, frame):
    raise TerminalResize

signal.signal(signal.SIGWINCH, handle_sigwinch)

def main():
    t = Terminal()
    while True:
        try:
            proc = Process(target=matrix_rain, daemon=True)
            proc.start()
            proc.join()
        except KeyboardInterrupt:
            print(t.clear())
            proc.terminate()
            break
        except TerminalResize:
            print(t.clear())
            proc.terminate()


if __name__ == '__main__':
    main()
