import os
import shutil
import subprocess

dock_files = "/lustre/fs6/lyu_lab/scratch/jlyu/dudez/DOCKING_GRIDS_AND_POSES"
for i in os.listdir(dock_files):
    os.makedirs(
        f"/lustre/fs6/lyu_lab/scratch/ichen/data/dudez_boltz_rescore/raw/xtal_lig",
        exist_ok=True,
    )
    os.makedirs(
        f"/lustre/fs6/lyu_lab/scratch/ichen/data/dudez_boltz_rescore/raw/rec_crg",
        exist_ok=True,
    )

    shutil.copy(
        f"{dock_files}/{i}/rec.crg.pdb",
        f"/lustre/fs6/lyu_lab/scratch/ichen/data/dudez_boltz_rescore/raw/rec_crg/{i}.pdb",
    )

    shutil.copy(
        f"{dock_files}/{i}/xtal-lig.pdb",
        f"/lustre/fs6/lyu_lab/scratch/ichen/data/dudez_boltz_rescore/raw/xtal_lig/{i}.pdb",
    )

    # Run the obabel command
    result = subprocess.run(
        [
            "obabel",
            "-ipdb",
            f"/lustre/fs6/lyu_lab/scratch/ichen/data/dudez_boltz_rescore/raw/xtal_lig/{i}.pdb",
            "-omol2",
            "-O",
            f"/lustre/fs6/lyu_lab/scratch/ichen/data/dudez_boltz_rescore/raw/xtal_lig/{i}.mol2",
            "--canonical",  # Canonical SMILES
            "-h",  # Add hydrogens
        ],
        capture_output=True,
        text=True,
    )

    # Check if command was successful
    if result.returncode == 0:
        print("Command executed successfully!")
        print("Output:", result.stdout)
    else:
        print("Command failed!")
        print("Error:", result.stderr)
