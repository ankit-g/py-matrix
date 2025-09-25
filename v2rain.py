from pyneorain import Bar, COLUMN_SPACING, TERMINAL_TOP_ROW, TERMINAL_LEFT_COLUMN, FRAMES_PER_SECOND, FIRST_ELEMENT_INDEX
from blessed import Terminal
from collections import deque
import asyncio
import signal
import sys

# Async-specific constants
QUEUE_SIZE = 64
SUCCESS_EXIT_CODE = 0


async def matrix_producer(t, aq):
    matrix = [[' ' for x in range(t.width)] for y in range(t.height)]
    columns = [deque([Bar(t, idx)]) if idx % COLUMN_SPACING == TERMINAL_TOP_ROW else None
                for idx in range(t.width)]
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
            if _q[FIRST_ELEMENT_INDEX].has_gone():
                _q.popleft()
        await aq.put(matrix)
        await asyncio.sleep(1/FRAMES_PER_SECOND)


async def matrix_consumer(t, aq):
    def print_term(matrix):
        with t.location(TERMINAL_TOP_ROW, TERMINAL_LEFT_COLUMN):
            print('\n'.join([''.join(row) for row in matrix]), end='\r')
    with t.hidden_cursor():
        while True:
            await asyncio.to_thread(print_term, await aq.get())

async def matrix_run():

    try:
        t = Terminal()
        aq = asyncio.Queue(QUEUE_SIZE)
        await asyncio.gather(
                    matrix_producer(t, aq),
                    matrix_consumer(t, aq),
                    matrix_consumer(t, aq)
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
                sys.exit(SUCCESS_EXIT_CODE)
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


if __name__ == '__main__':
    asyncio.run(main())
