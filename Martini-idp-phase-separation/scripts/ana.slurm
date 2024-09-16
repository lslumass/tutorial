#!/bin/bash
#SBATCH -c 100					  # Number of Cores per Task
#SBATCH --mem=8192 				  # Requested Memory
#SBATCH -t 1-00:00:0
#SBATCH -p cpu					  # Partition
#SBATCH -o slurm-%j.out  # %j = job ID
#SBATCH --mail-type=FAIL
#SBATCH --job-name=analysis

python -u clustering_mda_v2.py
