import sys

_RESCORE_INPUT_PATH = "/lustre/fs6/lyu_lab/scratch/ichen/projects/rescore/boltz2_rescore_input/src"
if _RESCORE_INPUT_PATH not in sys.path:
    sys.path.insert(0, _RESCORE_INPUT_PATH)

from boltz2_rescore_input.utils.mol2_utils import Mol2Utils
from boltz2_rescore_input.utils.rdkit_utils import RdkitUtils

class Ligand:
    def __init__(self, file_path):
        self.file_path = file_path
        if file_path.lower().endswith(".mol2"):
            self.init_mol2()

    def init_mol2(self):
        """
        Initializes the molecule from a mol2 file.
        """
        self.mol = Mol2Utils.read_single_mol2_file(self.file_path)
        if self.mol is None:
            raise ValueError(f"Failed to read mol2 file: {self.file_path}")
        try:
            self.smiles = RdkitUtils.get_smiles_from_mol(self.mol)
        except Exception as e:
            print(f"Failed to get SMILES for {self.file_path}: {e}")
            self.smiles = None
