from blessed import Terminal
import random
import time
import sys
import signal

import logging

logging.basicConfig(level=logging.DEBUG, filename='system.log')


class LandEnd(Exception):
    pass


class RiverEnd(Exception):
    pass


sanskrit = "ख,ग,घ,ङ,च,छ,ज,झ,ञ,ट,ठ,ड,ढ,ण,त,थ,द,ध,न,प,फ,ब,भ,म".split(",")
english = "a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,s,t,u,v,w,x,y,z".split(',')
numbers = "1,2,3,4,5,6,7,8,9,0".split(',')


class Land(object):

    def __init__(self, t):
        self.length = random.randint(1, int(t.height//1.5))
        self.pos = 0
        self.languages = sanskrit + english + numbers

    def get_pixel(self, t):
        if self.pos >= self.length:
            raise LandEnd
        self.pos += 1
        c = random.choice(self.languages)
        return t.green(c) if self.pos > 1 else t.white(c)


class River(object):

    def __init__(self, t):
        self.length = random.randint(1, t.height)
        self.pos = 0

    def get_pixel(self, t):
        if self.pos >= self.length:
            raise RiverEnd
        self.pos += 1
        return ' '


class Bar(object):

    def __init__(self, t, x):
        self.length = random.randint(10, t.height)
        self.total_length = self.length + random.randint(1, t.height)
        self.pos = 0
        self.t = t
        self.languages = sanskrit + english + numbers
        self.x = x
        self.has_u_neighbour = False  # upstairs neighbour

    def extend(self, scene):

        if self.has_fallen():
            return

        if self.pos < self.length:
            for i in range(self.pos):
                scene[i][self.x] = self.t.green(scene[i][self.x])
            scene[self.pos][self.x] = random.choice(self.languages)
        else:
            if self.pos < self.t.height:
                for i in range(self.pos):
                    scene[i][self.x] = self.t.green(scene[i][self.x])
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


class SceneLine(object):

    def __init__(self, t):
        self.objects = [random.choice(
            [Land]+[River]*4)(t) if not i % 2 else None for i in range(t.width)]

    def get_line(self, t):
        line = []
        for i, so in enumerate(self.objects):
            try:
                if not so:
                    line.append(' ')
                    continue
                line.append(so.get_pixel(t))
            except LandEnd:
                so = River(t)
                self.objects[i] = so
                line.append(so.get_pixel(t))
            except RiverEnd:
                so = Land(t)
                self.objects[i] = so
                line.append(so.get_pixel(t))

        return ''.join([c for c in line])


def matrix_os(t: Terminal, speed):
    """
      Matrix old style scrolling
    """
    sl = SceneLine(t)
    scene = ['' for y in range(t.height)]

    with t.hidden_cursor():
        while True:
            for y in range(t.height):
                with t.location(0, 0):
                    print("\n".join([line for line in scene]), end='\r')
                time.sleep(0.08)
                scene = (lambda r: [sl.get_line(t)
                         for _ in range(r)] + scene[:-r])(speed)


def matrix_ns(t: Terminal, speed):
    """
      Matrix new style scrolling
    """

    scene = [[' ' for x in range(t.width)] for y in range(t.height)]
    columns = [random.choice([[Bar(t, x)], None, None, None])
               if x % 2 else None for x in range(t.width)]

    with t.hidden_cursor():
        while True:
            for idx, bars in enumerate(columns):

                if not bars:
                    if idx % 2:
                        columns[idx] = random.choice(
                            [[Bar(t, idx)], None, None, None])
                    continue

                for b in bars:
                    b.extend(scene)
                    if b.has_bar_fallen() and b.has_u_neighbour == False:
                        columns[idx].append(Bar(t, idx))
                        b.has_u_neighbour = True
                    if b.has_fallen():
                        columns[idx].pop(0)

            with t.location(0, 0):
                print("\n".join([''.join(line) for line in scene]), end='\r')
            time.sleep(0.008)


def main():
    try:
        t = Terminal()
        print(t.clear())
#        matrix_os(t, speed=2)
        matrix_ns(t, speed=2)
    except KeyboardInterrupt:
        print(t.clear())
        sys.exit(0)


if __name__ == "__main__":
    main()
