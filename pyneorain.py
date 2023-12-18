import sys
import random
import signal
from blessed import Terminal
from functools import wraps
import asyncio


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
        if b.has_fully_extended() and not b.has_u_neighbour:
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
                print('\n'.join([''.join(line) for line in _scene]), end='\r')
        await asyncio.to_thread(paint, t, _scene)


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
            await asyncio.sleep(1/15)

async def matrix_run():

    try:
        q = asyncio.Queue(32)
        t = Terminal()
        scene = [[' ' for x in range(t.width)] for y in range(t.height)]
        columns = [None for x in range(t.width)]
        await asyncio.gather(
            matrix_ns(q, scene, columns),
            print_scene(q)
            )
    except asyncio.CancelledError:
        raise


sig_q = asyncio.Queue()

async def handle_sig(sigtype):
    await sig_q.put(sigtype)

async def async_main():
        t = Terminal()
        loop = asyncio.get_running_loop()
        loop.add_signal_handler(signal.SIGWINCH, lambda:asyncio.create_task(handle_sig(signal.SIGWINCH)))
        loop.add_signal_handler(signal.SIGINT, lambda:asyncio.create_task(handle_sig(signal.SIGINT)))
        mtask = asyncio.create_task(matrix_run())
        while True:
            sig = await sig_q.get()
            if sig == signal.SIGINT:
                print(t.clear())
                sys.exit(0)
            elif sig == signal.SIGWINCH:
                print(t.clear())
                try:
                    mtask.cancel()
                    await mtask
                except asyncio.CancelledError:
                    pass
                finally:
                    mtask = asyncio.create_task(matrix_run())

def main():
    asyncio.run(async_main())

if __name__ == "__main__":
    main()
