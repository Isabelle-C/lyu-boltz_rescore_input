#!/bin/bash
#SBATCH --job-name=msa_spark
#SBATCH --partition=lyu_b
#SBATCH --account=lyu_condo_bank
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4           # number of parallel Spark tasks
#SBATCH --mem=64G
#SBATCH --time=02:00:00


export PATH=/ru-auth/local/home/ichen/miniconda3/bin:$PATH

export PYSPARK_PYTHON=/lustre/fs6/lyu_lab/scratch/ichen/py_envs/cofolding_analysis/bin/python
export PYSPARK_DRIVER_PYTHON=$PYSPARK_PYTHON

# Verify both driver and worker will use the same interpreter
echo "[PYSPARK_PYTHON]" $PYSPARK_PYTHON
$PYSPARK_PYTHON -V  # Expect Python 3.10.x

# Set Spark local dirs (temporary)
export SPARK_LOCAL_DIRS=/lustre/fs6/lyu_lab/scratch/$USER/spark_tmp_$SLURM_JOB_ID
mkdir -p $SPARK_LOCAL_DIRS

# Thread config
export MMSEQS_THREADS=4


/lustre/fs6/lyu_lab/scratch/ichen/py_envs/cofolding_analysis/bin/python -u /lustre/fs6/lyu_lab/scratch/ichen/projects/rescore/boltz2_rescore_input/src/boltz2_rescore_input/src/boltz2/make_MSA.py
