import shutil


def write_lauch_script(job_name, input_parent: str):
    script_content = f"""#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --time=24:00:00
#SBATCH --gres=gpu:2
#SBATCH --partition=hpc_l40s
#SBATCH --mem-per-gpu=40G
#SBATCH --job-name={job_name}
#SBATCH --mail-user=ichen@rockefeller.edu
#SBATCH --mail-type=END,FAIL

AF3_dir="/lustre/fs6/lyu_lab/scratch/cyang/general_tutorial/AF3_pred"
export CUDA_VISIBLE_DEVICES=0,1

cd {input_parent}
mkdir -p $PWD/af_output
singularity exec \\
    --nv \\
    --bind $PWD \\
    --bind $PWD/af_inputs:/root/af_inputs \\
    --bind $PWD/af_output:/root/af_output \\
    --bind $AF3_dir/models:/root/models \\
    --bind $AF3_dir/databases:/root/public_databases \\
    $AF3_dir/image/alphafold3.sif \\
    /bin/bash -c "source run.sh"

"""
    with open(f"{input_parent}/launch.sbatch", "w") as f:
        f.write(script_content)


def copy_over_run_setup_single_recp(input_parent: str):
    shutil.copyfile("/lustre/fs6/lyu_lab/scratch/ichen/projects/cofolding_inputs/static/run_setup/run.sh", f"{input_parent}/run.sh")
    shutil.copyfile("/lustre/fs6/lyu_lab/scratch/ichen/projects/cofolding_inputs/static/run_setup/run_alphafold.py", f"{input_parent}/run_alphafold.py")
