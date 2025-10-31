from boltz.rescore.utils.pdb_utils import PdbUtils


class Protein:
    def __init__(self, file_path):
        self.file_path = file_path
        self.structure = PdbUtils.get_structure(file_path)

    def get_coords(self):
        coords = PdbUtils.get_coords_from_structure(self.structure)
        return coords

    def get_sequence(self):
        return PdbUtils.get_sequence_from_structure(self.structure)
