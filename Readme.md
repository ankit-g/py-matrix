# Matrix Terminal Screen-Saver Async Version

- This is just a humble 100-line Python module, not the full-blown Cmatrix implementation.

# do profiling like
 - kernprof -l pyneorain.py (line profiling)
 - python -m line_profiler pyneorain.py.lprof
 - mprof run pyneorain.py (Memory Profiling)
 - mprof plot

# publish to pypi
 - python -m build
 - twine upload dist/*

 ![Demo GIF](output.gif)
