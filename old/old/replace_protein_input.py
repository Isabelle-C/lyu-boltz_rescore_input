import json


def replace_protein_section(source_file, target_file):
    """
    Replace the protein section in target_file with the protein section from source_file
    """
    # Read the source file
    with open(source_file, "r") as f:
        source_data = json.load(f)

    # Read the target file
    with open(target_file, "r") as f:
        target_data = json.load(f)

    # Find and extract the protein section from source file
    source_protein = None
    for sequence in source_data.get("sequences", []):
        if "protein" in sequence:
            source_protein = sequence["protein"]
            break

    if source_protein is None:
        print("No protein section found in source file")
        return

    # Replace the protein section in target file
    for sequence in target_data.get("sequences", []):
        if "protein" in sequence:
            sequence["protein"] = source_protein
            break

    # Write the updated target file
    with open(target_file, "w") as f:
        json.dump(target_data, f, indent=4)

    print(f"Successfully replaced protein section in {target_file}")


# File paths


import os

dock_files = "/lustre/fs6/lyu_lab/scratch/jlyu/dudez/DOCKING_GRIDS_AND_POSES"
for i in os.listdir(dock_files):

    if i not in ["MK01", "PTN1", "ITAL", "XIAP"]:
        print(i)
        source_file = f"/ru-auth/local/home/ichen/lyu_scratch/data/dudez_af3/runs/{i}/af_output/{i.lower()}_xtal/{i.lower()}_xtal_data.json"
        target_file = f"/ru-auth/local/home/ichen/lyu_scratch/data/dudez_af3/runs/{i}/af_input/fold_input.json"
        # Execute the replacement
        replace_protein_section(source_file, target_file)
