import os
import re
from pathlib import Path

from rdkit import Chem


class Mol2Utils:
    """
    Utility class for handling mol2 files.
    """

    @staticmethod
    def read_single_mol2_file(file_path):
        mol = Chem.MolFromMol2File(file_path, sanitize=False)
        return mol

    @staticmethod
    def read_multiple_mol2_file(file_path):
        """
        Read mol2 file which contains >= 1 ligand.

        If file_path is a directory, read all .mol2 files in the directory.

        If file_path is a single .mol2 file, read that file containing multiple molecules and returns a list of RDKit molecule objects.
        """

        path = Path(file_path)

        def read_filepath(file_path) -> list:
            mols = []
            with open(file_path, "r") as f:
                mol_block = ""
                for line in f:
                    if "@<TRIPOS>MOLECULE" in line and mol_block:
                        mol = Chem.MolFromMol2Block(mol_block)
                        if mol:
                            mols.append(mol)
                        mol_block = line
                    else:
                        mol_block += line
                if mol_block:
                    mol = Chem.MolFromMol2Block(mol_block)
                    mols.append(mol)
            return mols

        def read_directory(directory_path) -> list:
            mols = []

            for filename in os.listdir(directory_path):
                if filename.endswith(".mol2"):
                    mol2_file_path = os.path.join(directory_path, filename)
                    mol = Chem.MolFromMol2File(mol2_file_path, sanitize=False)
                    if mol is not None:
                        mols.append(mol)
                    else:
                        raise ValueError(f"Failed to load {filename}")

            return mols

        if path.is_dir():
            print(f"{path} is a directory.")
            return read_directory(file_path)
        elif path.is_file():
            print(f"{path} is a file.")
            return read_filepath(file_path)
        else:
            raise ValueError(f"{path} is neither a file nor a directory.")

    @staticmethod
    def extract_smiles_from_mol2(mol2_file):
        with open(mol2_file, "r") as f:
            content = f.read()

        # Look for a line like: "##########               SMILES:   CC1=C(..."
        match = re.search(r"SMILES:\s*(\S+)", content)
        if match:
            return match.group(1)
        else:
            return None

    @staticmethod
    def scores_mol2(input_file, output_dir="output"):

        with open(input_file, "r") as infile:
            names = []
            scores = []

            current_lines = []
            current_name = None
            for line in infile:
                if line.startswith("##########                 Name:"):
                    current_lines = [line]
                    match = re.match(r"##########\s+Name:\s*(.*)", line)
                    if match:
                        current_name = match.group(1).strip()
                        names.append(current_name)
                else:
                    current_lines.append(line)
                    if line.startswith("##########         Total Energy:"):
                        match = re.match(r"##########\s+Total Energy:\s*(.*)", line)
                        if match:
                            score = match.group(1).strip()
                            scores.append(score)

            return names, scores
