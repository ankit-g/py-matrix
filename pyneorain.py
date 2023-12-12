import sys
import os
import time
import random
import signal
from blessed import Terminal
from copy import deepcopy
from multiprocessing import Process, Queue
from functools import wraps
import asyncio
import toml

# Load the config
config = toml.load('config.toml')

# Access the constants
languages = config['sanskrit']['characters'] +\
            config['english']['characters'] +\
            config['numbers']['characters'] +\
            config['greek']['characters'] +\
            config['kannada']['characters']

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
async def print_scene(q):
    t = Terminal()
    while True:
        _scene = await q.get()
        def paint(t, _scene):
            with t.location(0, 0):
                print('\n'.join([''.join(l) for l in _scene]), end='\r')
        await asyncio.to_thread(paint, t, _scene)
        await asyncio.sleep(1/15)


@process_ehandler
async def matrix_ns(q, scene, columns):
    """
      Matrix new style scrolling
    """
    t = Terminal()

    with t.hidden_cursor():
        while True:
            for idx, bars in enumerate(columns):
                if idx % 2:
                    continue
                if not bars:
                    columns[idx] = random.choice(
                        [[Bar(t, idx)]] + [None]*3)
                    continue
                worker(bars, scene, columns, idx, t)
            await q.put(scene)
            await asyncio.sleep(0)


async def async_main():

    q = asyncio.Queue(24)
    t = Terminal()
    scene = [[' ' for x in range(t.width)] for y in range(t.height)]
    columns = [None for x in range(t.width)]
    await asyncio.gather(
            matrix_ns(q, scene, columns),
            print_scene(q)
            )

def handle_sighup(signal, frame):
    raise TerminalResize

def main():
    try:
        t = Terminal()
        signal.signal(signal.SIGWINCH, handle_sighup)
        asyncio.run(async_main())
    except KeyboardInterrupt:
        print(t.clear())
        sys.exit(0)
    except TerminalResize:
        print(t.clear())
        main()


if __name__ == "__main__":
    main()
