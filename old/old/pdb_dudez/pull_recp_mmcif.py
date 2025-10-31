from Bio.PDB import PDBList

# Create an instance of the PDBList class
pdb_list = PDBList()

# Specify the PDB ID of the structure you want to download
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

# Download the MMCIF file using the retrieve_pdb_file method
for pdb_id in files.values():
    pdb_filename = pdb_list.retrieve_pdb_file(
        pdb_id, pdir="data/PDB_files", file_format="mmCif"
    )

    # Print the name of the downloaded file
    print(pdb_filename)
