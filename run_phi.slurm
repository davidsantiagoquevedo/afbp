#!/bin/bash
#SBATCH --job-name=run_phi          # Job name
#SBATCH --output=run_phi.out        # Standard output log
#SBATCH --error=run_phi.err         # Standard error log
#SBATCH --ntasks=1                  # Number of tasks (1 for a single python script)
#SBATCH --cpus-per-task=6           # Number of CPU cores needed
#SBATCH --time=01:00:00             # Max runtime (hh:mm:ss)
#SBATCH --partition=normal          # Partition to submit to (change if needed)

# Activate python virtual environment
source /nethome/1184938/venvs/phys/bin/activate


# Run the Python script 
~/venvs/phys/bin/python3 scripts/run_phi.py
