#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=0
#SBATCH --time=100:00:00
#SBATCH --job-name=step3
#SBATCH --output=step3

source ~/.bashrc
conda activate cdat_lite
cd /carnegie/nobackup/scratch/lduan/clab_rate_of_warming

python analysis_spatial_step3.py
