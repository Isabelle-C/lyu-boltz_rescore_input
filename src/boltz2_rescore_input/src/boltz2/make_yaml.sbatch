#!/bin/bash
#SBATCH --job-name=msa_spark
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4           # number of parallel Spark tasks
#SBATCH --mem=64G
#SBATCH --time=02:00:00


export PATH=/ru-auth/local/home/ichen/miniconda3/bin:$PATH

export PYSPARK_PYTHON=/lustre/fs6/lyu_lab/scratch/ichen/py_envs/cofolding_analysis/bin/python
export PYSPARK_DRIVER_PYTHON=$PYSPARK_PYTHON

/lustre/fs6/lyu_lab/scratch/ichen/py_envs/cofolding_analysis/bin/python -u /lustre/fs6/lyu_lab/scratch/ichen/projects/rescore/boltz2_rescore_input/src/boltz2_rescore_input/src/boltz2/make_yaml.py
