import json
import os


def replace_seed_section(source_file, target_file):
    """
    Replace the protein section in target_file with the protein section from source_file
    """
    # Read the source file
    with open(source_file, "r") as f:
        source_data = json.load(f)

    # Find and extract the protein section from source file
    source_data["modelSeeds"] = [4, 9, 8, 31, 20]

    # Write the updated target file
    with open(target_file, "w") as f:
        json.dump(source_data, f, indent=4)

    print(f"Successfully replaced seed section in {target_file}")


dock_files = "/lustre/fs6/lyu_lab/scratch/jlyu/dudez/DOCKING_GRIDS_AND_POSES"
for i in os.listdir(dock_files):
    source_file = f"/ru-auth/local/home/ichen/lyu_scratch/data/dudez_af3/runs_seed1/{i}/af_output/{i.lower()}_xtal/{i.lower()}_xtal_data.json"
    target_file = f"/ru-auth/local/home/ichen/lyu_scratch/data/dudez_af3/runs/{i}/af_input/fold_input.json"

    replace_seed_section(source_file, target_file)
