import sys
import os


_COFOLDING_INPUT_PATH = "/lustre/fs6/lyu_lab/scratch/ichen/projects/cofolding_inputs/src"
if _COFOLDING_INPUT_PATH not in sys.path:
    sys.path.insert(0, _COFOLDING_INPUT_PATH)

from cofolding_inputs.utils.mol2_util import split_mol2
from cofolding_inputs.rescore.data_paths import docking_results_path, split_mol2_output_path


for i in os.listdir(docking_results_path):
    split_mol2(
        f"{docking_results_path}/{i}/poses.mol2",
        output_dir=f"{split_mol2_output_path}/{i}",
    )
