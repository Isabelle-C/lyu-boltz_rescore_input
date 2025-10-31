import string

from Bio.PDB import PDBParser
from Bio.SeqUtils import seq1


class PdbUtils:
    """
    Utility class for handling PDB files.
    """

    @staticmethod
    def get_structure(file_path):
        """Parses the PDB file and returns the structure object."""
        parser = PDBParser(QUIET=True)
        structure = parser.get_structure("rec", file_path)
        return structure

    @staticmethod
    def get_coords_from_structure(structure):
        """
        Extracts coordinates from a PDB structure.
        """
        coords = []
        for model in structure:
            for idx, chain in enumerate(model):
                chain_letter = string.ascii_uppercase[idx]
                res_id = 0
                for residue in chain:
                    for atom in residue:
                        if atom.name.startswith("H"):  # Skip hydrogens
                            continue
                        # print((
                        #     chain_letter,
                        #     res_id,
                        #     residue.resname,
                        #     atom.name,
                        #     atom.coord[0],
                        #     atom.coord[1],
                        #     atom.coord[2],
                        # ))
                        coords.append(
                            (
                                chain_letter,
                                res_id,
                                atom.name,
                                atom.coord[0],
                                atom.coord[1],
                                atom.coord[2],
                                residue.resname,
                            )
                        )
                    res_id += 1
        return coords

    @staticmethod
    def get_sequence_from_structure(structure):
        """
        Extracts the sequence from a PDB structure.
        """
        chain_sequences = {}
        for model in structure:
            for idx, chain in enumerate(model):
                chain_letter = string.ascii_uppercase[idx]
                residue_sequence = []
                for residue in chain:
                    residue_sequence.append(residue.resname)
                one_letter = "".join([seq1(aa) for aa in residue_sequence])
                chain_sequences[chain_letter] = one_letter

        ligand_letter = string.ascii_uppercase[idx + 1]
        return chain_sequences, ligand_letter
