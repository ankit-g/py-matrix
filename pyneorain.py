import sys
import os
import time
import random
import signal
import logging
from blessed import Terminal
from copy import deepcopy
from multiprocessing import Process, Queue
from functools import wraps

logging.basicConfig(level=logging.DEBUG, filename='system.log')

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


class TerminalResize(Exception):
    pass


def process_ehandler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            t = Terminal()
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            print(t.clear())
            sys.exit(0)
    return wrapper


class Bar(object):

    def __init__(self, t, x):
        self.length = random.randint(10, t.height//1.5)
        self.total_length = self.length + random.randint(5, t.height//1.5)
        self.pos = 0
        self.t = t
        self.languages = languages
        self.x = x
        self.has_u_neighbour = False  # upstairs neighbour

    def extend(self, scene):

        def go_green(x):
            return '\x1b[32m' + x + '\x1b(B\x1b[m' if self.t.green not in x else x

        if self.has_gone():
            return

        if self.pos < self.length:
            scene[self.pos-1][self.x] = go_green(scene[self.pos-1][self.x])
            scene[self.pos][self.x] = random.choice(self.languages)
        else:
            if self.pos < self.t.height:
                scene[self.pos-1][self.x] = go_green(scene[self.pos-1][self.x])
                scene[self.pos][self.x] = random.choice(self.languages)
            if self.pos - self.length < self.t.height:
                scene[self.pos-self.length][self.x] = ' '
        self.pos += 1

    def has_gone(self):
        return self.pos >= self.t.height + self.total_length

    def has_fully_extended(self):
        return self.pos >= self.total_length


def worker(bars, scene, columns, idx, t):
    for b in bars:
        b.extend(scene)
        if b.has_fully_extended() and b.has_u_neighbour == False:
            columns[idx].append(Bar(t, idx))
            b.has_u_neighbour = True
        if b.has_gone():
            columns[idx].pop(0)


@process_ehandler
def print_scene(q):
    t = Terminal()
    while True:
        _scene = q.get()
        with t.location(0, 0):
            print('\n'.join([''.join(l) for l in _scene]), end='\r')
        time.sleep(1/30)


@process_ehandler
def matrix_ns(q, scene, columns):
    """
      Matrix new style scrolling
    """
    t = Terminal()

    with t.hidden_cursor():
        while True:
            if q.full():
                time.sleep(1/60)
                continue
            for idx, bars in enumerate(columns):
                if idx % 2:
                    continue
                if not bars:
                    columns[idx] = random.choice(
                        [[Bar(t, idx)]] + [None]*3)
                    continue
                worker(bars, scene, columns, idx, t)
            q.put(scene)


def main():
    try:
        q = Queue(2)
        t = Terminal()
        scene = [[' ' for x in range(t.width)] for y in range(t.height)]
        columns = [None for x in range(t.width)]

        def handle_sighup(signal, frame):
            raise TerminalResize

        signal.signal(signal.SIGWINCH, handle_sighup)

        print(t.clear())
        procs = [
            Process(target=print_scene, args=(q,), daemon=True),
            Process(target=matrix_ns, args=(q, scene, columns), daemon=True),
        ]

        for p in procs:
            p.start()
        for p in procs:
            p.join()
    except KeyboardInterrupt:
        print(t.clear())
        sys.exit(0)
    except TerminalResize:
        for p in procs:
            p.terminate()
        del t, q, procs
        main()


if __name__ == "__main__":
    main()
