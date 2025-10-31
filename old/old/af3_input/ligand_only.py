import json
import os

import yaml

with open(
    "/lustre/fs6/lyu_lab/scratch/ichen/projects/cofolding_analysis/src/cofolding_analysis/database/configs/analysis_set/dudez/receptors.yaml",
    "r",
    encoding="utf-8",
) as f:
    config = yaml.safe_load(f)
receptors = config.get("recp_names", None)

ligand_info = None

for recp_name in receptors:
    input_path = f"/lustre/fs6/lyu_lab/scratch/kmenon01/af3/testing/charge_matched_dude/{recp_name.lower()}/output"

    output_folder = f"/lustre/fs6/lyu_lab/scratch/ichen/data/af3_eval/ligand_only/{recp_name}/af_input"
    os.makedirs(output_folder, exist_ok=True)

    for ligand in os.listdir(input_path):

        input_file = f"{input_path}/{ligand}/af_input/fold_input.json"

        if not os.path.exists(f"{output_folder}/{ligand}.json") and (
            os.path.exists(input_file)
        ):

            with open(input_file, "r") as f:
                data = json.load(f)

                name = data["name"]
                sequence = data["sequences"]

                for i in sequence:
                    if "ligand" in i.keys():
                        ligand_info = i

                if ligand_info is None:
                    raise ValueError(f"No ligand info found in {input_file}")

                new_sequence = [ligand_info]

                ligand_info = None

                ligand_only_data = {
                    "dialect": data["dialect"],
                    "version": data["version"],
                    "name": name,
                    "sequences": new_sequence,
                    "modelSeeds": data["modelSeeds"],
                }

            with open(f"{output_folder}/{ligand}.json", "w") as f:
                json.dump(ligand_only_data, f, indent=4)
