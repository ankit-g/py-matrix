# Embrace Reality. Enter the Matrix, Neo.

-  "Let me tell you why you're here. You're here because you know something.
    What you know, you can't explain. But you feel it. You've felt it your entire life.
    That there's something wrong with the world.
    You don't know what it is, but it's there, like a splinter in your mind, driving you mad."

- This is just a humble 100 line python module, not the full-blown cmatrix implementation.
    But hey, who wants to understand all that c code anyway? This module is much easier on the eyes and brain.

- So what's next? Well, this project is just getting started and is actively seeking more contributions.
    So if you have any ideas or improvements, we'd love to hear from you. Let's make this the best Matrix screensaver around!


# do profiling like
 - kernprof -l pyneorain.py (line profiling)
 - python -m line_profiler pyneorain.py.lprof
 - mprof run pyneorain.py (Memory Profiling)
 - mprof plot

# publish to pypi
 - python setup.py sdist
 - twine upload dist/*
