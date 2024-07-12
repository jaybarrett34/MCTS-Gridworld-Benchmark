# Requires virtual environment

Windows:

- python -m venv venv
- venv\Scripts\activate

Linux, MacOS

- python -m venv venv
- source venv/bin/activate

# Run benchmarks from root dir

- export PYTHONPATH=$PYTHONPATH:../MCTS-Gridworld-Benchmark

Fixes this error message:
'''
Traceback (most recent call last):
File "../MCTS-Gridworld-Benchmark/tests/benchmarks.py", line 3, in <module>
from algorithms.uct import UCT # Assuming UCT is your algorithm class
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ModuleNotFoundError: No module named 'algorithms'
'''

# Implemented:

- Printouts
- Components
- UCT
- MENTS (incomplete)
- BTS (incomplet)

# Issues:

- UCT throws an error if the map is all open
- MENTS does not work, cycles between 0, 1, and 4. May incorrectly find goal or just crash
- BTS does not work. I am at a loss
- DENTS just not implemented.
