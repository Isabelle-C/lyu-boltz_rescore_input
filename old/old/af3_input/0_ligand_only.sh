#!/bin/bash

#SBATCH --job-name="smiles_db"
#SBATCH --time=24:00:00
#SBATCH --cpus-per-task=8
#SBATCH --mem-per-cpu=32G
#SBATCH --mail-user=ichen@rockefeller.edu
#SBATCH --mail-type=END,FAIL

# #SBATCH --partition=lyu_b
# #SBATCH --account=lyu_condo_bank

export PATH=/ru-auth/local/home/ichen/miniconda3/bin:$PATH

# Initialize conda properly for bash scripts
source /ru-auth/local/home/ichen/miniconda3/etc/profile.d/conda.sh

# Activate the environment using conda activate (not source activate)
conda activate /lustre/fs6/lyu_lab/scratch/ichen/py_envs/cofolding_analysis


export PATH=/lustre/fs6/lyu_lab/scratch/ichen/py_envs/cofolding_analysis/bin:$PATH
/lustre/fs6/lyu_lab/scratch/ichen/py_envs/cofolding_analysis/bin/python /lustre/fs6/lyu_lab/scratch/ichen/cofolding_analysis/src/cofolding_analysis/af3_input/ligand_only.py