#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --time=05:00:00
#SBATCH --gres=gpu:4
#SBATCH -p hpc_l40s
#SBATCH --mem-per-gpu=40G
#SBATCH --job-name=perspective
#SBATCH --mail-user=ichen@rockefeller.edu
#SBATCH --mail-type=END,FAIL

export CUDA_VISIBLE_DEVICES=0,1,2,3
export PATH=/ru-auth/local/home/ichen/miniconda3/bin:$PATH
export XDG_CACHE_HOME=/lustre/fs6/lyu_lab/scratch/ichen/boltz2_cache/.cache
export XDG_CONFIG_HOME=/lustre/fs6/lyu_lab/scratch/ichen/boltz2_cache/.config
export TRITON_CACHE_DIR=/lustre/fs6/lyu_lab/scratch/ichen/boltz2_cache/.triton_cache
source activate boltz2

cd /lustre/fs6/lyu_lab/scratch/ichen/data/boltz2_perspective
boltz predict /lustre/fs6/lyu_lab/scratch/ichen/data/boltz2_perspective/ligand_only_configs --use_msa_server --cache /lustre/fs6/lyu_lab/scratch/ichen/boltz2_cache