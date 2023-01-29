from blessed import Terminal
import random
import time
import sys
import signal


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


def matrix(t: Terminal, speed):
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


def main():
    try:
        t = Terminal()
        print(t.clear())
        matrix(t, speed=2)
    except KeyboardInterrupt:
        print(t.clear())
        sys.exit(0)


if __name__ == "__main__":
    main()
