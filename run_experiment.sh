#!/bin/bash
#SBATCH -p plgrid
#SBATCH -t 65:00:00

source venv/bin/activate
python3 main.py bier127 30 1 0
