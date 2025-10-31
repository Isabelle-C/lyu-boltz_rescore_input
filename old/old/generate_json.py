import json
import os
import string

import pandas as pd
from boltz.rescore.load.ligand import Ligand
from boltz.rescore.load.protein import Protein

af3_input_dir = "/lustre/fs6/lyu_lab/scratch/ichen/data/dudez_af3/input"
os.makedirs(af3_input_dir, exist_ok=True)

ccd_df = pd.read_csv(
    "/ru-auth/local/home/ichen/lyu_scratch/rescore/input/af3/pdb_dudez/completed_smiles.csv"
)

files = {
    "aa2ar": "3eml",
    "abl1": "2hzi",
    "aces": "1e66",
    "ada": "2e1w",
    "adrb2": "3ny8",
    "ampc": "1l2s",
    "andr": "2am9",
    "csf1r": "3krj",
    "cxcr4": "3odu",
    "def": "1lru",
    "drd4": "5wiu",
    "egfr": "2rgp",
    "fa10": "3kl6",
    "fa7": "1w7x",
    "fabp4": "2nnq",
    "fgfr1": "3c4f",
    "fkb1a": "1j4h",
    "glcm": "2v3f",
    "hdac8": "3f07",
    "hivpr": "1xl2",
    "hmdh": "3ccw",
    "hs90a": "1uyg",
    "ital": "2ica",
    "kit": "3g0e",
    "kith": "2b8t",
    "lck": "2of2",
    "mapk2": "3m2w",
    "mk01": "2ojg",
    "mt1": "6me4",
    "nram": "1b9v",
    "parp1": "3l3m",
    "plk1": "2owb",
    "ppara": "2p54",
    "ptn1": "2azr",
    "pur2": "1njs",
    "reni": "3g6z",
    "rock1": "2etr",
    "src": "3el8",
    "thrb": "1ype",
    "try1": "2ayw",
    "tryb1": "2zec",
    "urok": "1sqt",
    "xiap": "3hl5",
}


def get_ligand_name(recp_name):
    """Get ligand_name for a given recp_name from the CSV"""
    # Convert to uppercase for case-insensitive matching
    match = ccd_df[ccd_df["recp_name"].str.upper() == recp_name.upper()]

    if not match.empty:
        return match.iloc[0]["ligand_name"]
    else:
        print(f"No ligand found for receptor: {recp_name}")
        return None


def read_fasta_as_dict(fasta_file_path):
    """
    Read a FASTA file and return it as a dictionary.

    Args:
        fasta_file_path (str): Path to the FASTA file

    Returns:
        dict: Dictionary with headers as keys and sequences as values
    """
    fasta_dict = {}

    try:
        with open(fasta_file_path, "r", encoding="utf-8") as file:
            current_header = None
            current_sequence = []

            for line in file:
                line = line.strip()

                if line.startswith(">"):
                    # If we have a previous sequence, save it
                    if current_header is not None:
                        fasta_dict[current_header] = "".join(current_sequence)

                    # Start new sequence
                    current_header = line[1:]  # Remove the '>' character
                    current_sequence = []

                elif line:  # Skip empty lines
                    current_sequence.append(line)

            # Don't forget the last sequence
            if current_header is not None:
                fasta_dict[current_header] = "".join(current_sequence)

    except FileNotFoundError:
        print(f"Error: File {fasta_file_path} not found.")
        return {}
    except IOError as e:
        print(f"Error reading file: {e}")
        return {}

    return fasta_dict


def af3_json(ccd, k, v, name):
    print("-------" * 6)

    fasta_file = f"/ru-auth/local/home/ichen/lyu_scratch/data/FASTA_files/{v}.fasta"
    fasta_dict = read_fasta_as_dict(fasta_file)

    protein = Protein(
        f"/lustre/fs6/lyu_lab/scratch/ichen/data/dudez_boltz_rescore/raw/rec_crg/{k.upper()}.pdb"
    )
    seq_dict, _ = protein.get_sequence()

    final_seq = []

    if len(seq_dict) > 1:
        if fasta_dict:
            for header, sequence in fasta_dict.items():
                print(f"Header: {header}, Sequence Length: {len(sequence)}")

    chain_iter = iter(string.ascii_uppercase)
    for _, seq in fasta_dict.items():
        protein_chains = {}
        protein_chains["id"] = next(chain_iter)

        protein_chains["sequence"] = seq
        final_seq.append({"protein": protein_chains})

    ligand = {}
    ligand["id"] = next(chain_iter)
    ligand["ccdCodes"] = [ccd]
    final_seq.append({"ligand": ligand})
    return {
        "name": name,
        "sequences": final_seq,
        "modelSeeds": [4, 9, 8, 31, 20],
        "dialect": "alphafold3",
        "version": 1,
    }


for k, v in files.items():
    full_data = af3_json(get_ligand_name(k), k, v, f"{k}_xtal")
    with open(f"{af3_input_dir}/{k}_xtal.json", "w") as f:
        json.dump(full_data, f, indent=4)
