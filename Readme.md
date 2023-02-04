#Welcome to the Matrix

- This is just a humble 100 line python module, not the full-blown cmatrix implementation.
    But hey, who wants to understand all that c code anyway? This module is much easier on the eyes and brain.

- So what's next? Well, this project is just getting started and is actively seeking more contributions.
    So if you have any ideas or improvements, we'd love to hear from you. Let's make this the best Matrix screensaver around!

# Algothim for New Style Scroll

- screen is a matrix which is devided into columns and each column has a random length.
- each column either extends or falls.
- columns keep extending from the base (x=n, y=0) of the screen until their legth has been reached.
    write column extend algorithm.
- once the columns have reached their length they start falling.
    write down column fall algorithm

# do profiling like
 - kernprof -l matrix.py (line profiling)
 - python -m line_profiler matrix.py.lprof
 - mprof run matrix.py (Memory Profiling)
 - mprof plot

