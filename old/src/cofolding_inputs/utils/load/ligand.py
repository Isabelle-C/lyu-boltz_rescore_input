from boltz.rescore.utils.mol2_utils import Mol2Utils
from boltz.rescore.utils.pdb_utils import PdbUtils
from boltz.rescore.utils.rdkit_utils import RdkitUtils


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

        # smiles = RdkitUtils.get_smiles_from_mol(self.mol)
        # if Mol2Utils.extract_smiles_from_mol2(file_path) == smiles:
        #     self.smiles = smiles
        # else:
        #     raise ValueError(
        #         f"Mismatch! From RDkit: {smiles} From regex: {Mol2Utils.extract_smiles_from_mol2(file_path)}"
        #     )
