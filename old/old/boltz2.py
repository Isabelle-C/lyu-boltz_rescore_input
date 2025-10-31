import os


class Batch:
    @staticmethod
    def write_yaml_line_by_line(filepath: str, data: dict):
        """Write a YAML file line by line from a dictionary"""
        with open(filepath, "w") as f:
            for key, value in data.items():
                if isinstance(value, dict):
                    f.write(f"{key}:\n")
                    for sub_key, sub_value in value.items():
                        f.write(f"  {sub_key}: {sub_value}\n")
                else:
                    f.write(f"{key}: {value}\n")


with open(
    "/lustre/fs6/lyu_lab/scratch/ichen/data/boltz2_perspective/raw/results-2.txt", "r"
) as f:
    lines = f.readlines()

zinc_ids = []
smiles = []

# Skip the first line which is a header
l = lines[0].replace("\n", "")
split_list = l.split(" ")
print(split_list)
header = split_list

for l in lines[1:]:
    l = l.replace("\n", "")
    split_list = l.split(" ")

    zinc_ids.append(split_list[0])
    smiles.append(split_list[1])


for i, j in zip(zinc_ids, smiles):
    boltz_config = {
        "version": 1,
        "sequences": [
            {
                "protein": {
                    "id": "A",
                    "sequence": "GPGGSSMGTLGARRGLEWFLGFYFLSHIPITLLMDLQGVLPRDLYPVELRNLQQWYIEEFKDPLLQTPPAWFKSFLFCELVFQLPFFPIAAYAFFKGGCKWIRTPAIIYSVHTMTTLIPILSTLLLDDFSKASHFRGQGPKTFQERLFLISVYIPYFLIPLILLLFMVRNPYYK",
                    "msa": "/lustre/fs6/lyu_lab/scratch/ichen/data/boltz2_perspective/boltz_results_configs/msa/ZINCkQ00000C3eFS_unpaired_tmp_env/uniref.a3m",
                }
            },
            {"ligand": {"id": "B", "smiles": j}},
        ],
        "properties": [{"affinity": {"binder": "B"}}],
    }
    yaml_file = (
        f"/lustre/fs6/lyu_lab/scratch/ichen/data/boltz2_perspective/configs/{i}.yaml"
    )

    if not os.path.exists(yaml_file):
        print("Creating file")
        Batch.write_yaml_line_by_line(yaml_file, boltz_config)
