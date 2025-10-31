def extract_residue_name(pdb_line):
    """
    Extract residue name from a PDB ATOM line
    Example line: ATOM      1  C1  ZMA B 401      30.767  36.799  63.252  1.00104.51           C
    """
    if pdb_line.startswith("ATOM"):
        # Residue name is in columns 17-20 (0-based indexing)
        residue_name = pdb_line[17:20].strip()
        return residue_name
    return None


import os

import pandas as pd

df_path = (
    "/ru-auth/local/home/ichen/lyu_scratch/rescore/input/af3/pdb_dudez/xtal_lig.csv"
)
df_data = {"xtal_name": [], "recp_name": []}


for i in os.listdir("/lustre/fs6/lyu_lab/scratch/jlyu/dudez/DOCKING_GRIDS_AND_POSES"):
    with open(
        os.path.join(
            f"/lustre/fs6/lyu_lab/scratch/jlyu/dudez/DOCKING_GRIDS_AND_POSES/{i}/xtal-lig.pdb"
        )
    ) as f:
        lines = f.readlines()
        line = lines[0]

        residue_name = extract_residue_name(line)
        df_data["xtal_name"] += [residue_name]
        df_data["recp_name"] += [i]

df = pd.DataFrame(df_data)
df.to_csv(df_path)
