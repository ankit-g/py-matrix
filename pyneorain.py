from blessed import Terminal
import random
import time
import sys
import signal
import numpy as np
import logging
import asyncio

logging.basicConfig(level=logging.DEBUG, filename='system.log')

sanskrit = "ख,ग,घ,ङ,च,छ,ज,झ,ञ,ट,ठ,ड,ढ,ण,त,थ,द,ध,न,प,फ,ब,भ,म".split(",")
english = "a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,s,t,u,v,w,x,y,z".split(',')
numbers = "1,2,3,4,5,6,7,8,9,0".split(',')
greek = ['α', 'β', 'γ', 'δ', 'ε', 'ζ', 'η', 'θ', 'ι', 'κ', 'λ', 'μ', 'ν', 'ξ', 'ο', 'π', 'ρ', 'σ', 'τ', 'υ', 'φ', 'χ', 'ψ', 'ω']
kannada = ['ಅ', 'ಆ', 'ಇ', 'ಈ', 'ಎ', 'ಏ', 'ಐ', 'ಒ', 'ಓ', 'ಔ', 'ಕ', 'ಖ', 'ಗ', 'ಘ', 'ಙ', 'ಚ', 'ಛ', 'ಜ',]

languages = english + kannada + sanskrit + greek + numbers

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

        if self.has_fallen(): return

        if self.pos < self.length:
            scene[self.pos-1, self.x] = go_green(scene[self.pos-1, self.x])
            scene[self.pos][self.x] = random.choice(self.languages)
        else:
            if self.pos < self.t.height:
                scene[self.pos-1, self.x] = go_green(scene[self.pos-1, self.x])
                scene[self.pos][self.x] = random.choice(self.languages)
            if self.pos - self.length < self.t.height:
                scene[self.pos-self.length][self.x] = ' '
        self.pos += 1

    def has_fallen(self):
        return self.pos >= self.t.height + self.length

    def has_bar_fallen(self):
        return self.pos >= self.total_length

    def is_complete(self):
        return self.pos >= self.length and (self.pos - self.length) >= self.total_length


def worker(bars, scene, columns, idx, t):
    for b in bars:
        b.extend(scene)
        if b.has_bar_fallen() and b.has_u_neighbour == False:
            columns[idx].append(Bar(t, idx))
            b.has_u_neighbour = True
        if b.has_fallen():
            columns[idx].pop(0)

#@profile
async def matrix_ns(t: Terminal):
    """
      Matrix new style scrolling
    """
    scene = np.array([[' ' for x in range(t.width)] for y in range(t.height)], dtype=object)
    columns = [random.choice([[Bar(t, x)]]+[None]*3)
               if x % 2 else None for x in range(t.width)]

    with t.hidden_cursor():
        while True:
            for idx, bars in enumerate(columns):
                if idx % 2: continue
                if not bars:
                    columns[idx] = random.choice(
                            [[Bar(t, idx)]] + [None]*3)
                    continue
                worker(bars, scene, columns, idx, t)
            with t.location(0, 0):
                print('\n'.join([''.join(line) for line in scene]), end='\r')
            await asyncio.sleep(0.03)

def main():
    try:
        t = Terminal()
        print(t.clear())
        asyncio.run(matrix_ns(t))
    except KeyboardInterrupt:
        print(t.clear())
        sys.exit(0)


if __name__ == "__main__":
    main()
