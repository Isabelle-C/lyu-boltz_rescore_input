from rdkit import Chem


class RdkitUtils:
    @staticmethod
    def get_list_of_atoms_from_mol(mol):
        return [atom.GetSymbol() for atom in mol.GetAtoms()]

    @staticmethod
    def get_num_atoms(mol):
        return mol.GetNumAtoms()

    @staticmethod
    def get_chemical_name_from_mol(mol):
        if mol.HasProp("_Name"):
            return mol.GetProp("_Name").split()[0]
        else:
            return "Unknown"

    @staticmethod
    def get_smiles_from_mol(mol):
        return Chem.MolToSmiles(mol, kekuleSmiles=True, canonical=False)

    @staticmethod
    def get_coord_from_mol(mol) -> list:
        coords = []
        conf = mol.GetConformer()  # Get 3D conformer
        for atom in mol.GetAtoms():
            idx = atom.GetIdx()
            pos = conf.GetAtomPosition(idx)
            coords.append((pos.x, pos.y, pos.z))

            # Alternatively
            # coords = {}
            # coords[atom.GetSymbol() + str(idx)] = (pos.x, pos.y, pos.z)

        return coords
