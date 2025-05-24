#!/bin/bash

# Activate virtual environment and run SMA crossover strategy
source .venv/bin/activate
PYTHONPATH=$PYTHONPATH:. python3 strategies/sma_crossover.py 