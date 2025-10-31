import os
import shutil

pkg_folder_path = "/lustre/fs6/lyu_lab/scratch/ichen/projects/cofolding_analysis/src/cofolding_analysis"
run_alphafold_script = f"{pkg_folder_path}/af3_run_dir/run_setup/run_alphafold.py"
run_sh_script = f"{pkg_folder_path}/af3_run_dir/run_setup/run.sh"
folder_run = "/lustre/fs6/lyu_lab/scratch/ichen/data/ampc_s2_d4/af3_ligand_only"


def make_target_dir(receptor_name):
    return f"{folder_run}/{receptor_name}"


def setup_af3_run(receptor_name):
    """
    1. Create directory structure
    2. Copy and rename JSON file
    """

    target_dir = make_target_dir(receptor_name)

    try:
        shutil.copy2(
            run_alphafold_script,
            f"{target_dir}/run_alphafold.py",
        )

        if os.path.exists(f"{target_dir}/run.sh"):
            os.remove(f"{target_dir}/run.sh")
        shutil.copy2(
            run_sh_script,
            f"{target_dir}/run.sh",
        )

    except FileNotFoundError:
        print(f"Error: Source file not found")
    except Exception as e:
        print(f"Error: {e}")


def make_sbatch(recp_name):
    """ """
    sbatch_lines = [
        "#! /bin/bash",
        "#SBATCH --nodes=1",
        "#SBATCH --ntasks=1",
        "#SBATCH --cpus-per-task=8",
        "#SBATCH --time=12:00:00",
        "#SBATCH --gres=gpu:2",
        "#SBATCH -p hpc_l40s",
        "#SBATCH --mem-per-gpu=40G",
        f"#SBATCH --job-name={recp_name}_af3",
        "#SBATCH --mail-user=ichen@rockefeller.edu",
        "#SBATCH --mail-type=END,FAIL",
        'AF3_dir="/lustre/fs6/lyu_lab/scratch/cyang/general_tutorial/AF3_pred"',
        "export CUDA_VISIBLE_DEVICES=0,1",
        "",
        f"cd {make_target_dir(recp_name)}",
        "mkdir -p $PWD/af_output",
        "singularity exec \\",
        "    --nv \\",
        "    --bind $PWD \\",
        "    --bind $PWD/af_input:/root/af_input \\",
        "    --bind $PWD/af_output:/root/af_output \\",
        "    --bind $AF3_dir/models:/root/models \\",
        "    --bind $AF3_dir/databases:/root/public_databases \\",
        "    $AF3_dir/image/alphafold3.sif \\",
        '    /bin/bash -c "source run.sh"',
    ]

    return sbatch_lines


for i in os.listdir(folder_run):
    setup_af3_run(i)

    sbatch_content = make_sbatch(i)
    sbatch_file = f"{make_target_dir(i)}/launch.sbatch"
    with open(sbatch_file, "w") as f:
        for line in sbatch_content:
            f.write(line + "\n")
    print(f"Created SBATCH file: {sbatch_file}")
