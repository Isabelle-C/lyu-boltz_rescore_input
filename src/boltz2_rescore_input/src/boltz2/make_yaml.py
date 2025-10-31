import os
import sys

from pyspark.sql import SparkSession
from pyspark.sql.functions import asc

_COFOLDING_PATH = "/lustre/fs6/lyu_lab/scratch/ichen/projects/cofolding_analysis/src"
if _COFOLDING_PATH not in sys.path:
    sys.path.insert(0, _COFOLDING_PATH)

_COFOLDING_EXPERIMENT_PATH = "/lustre/fs6/lyu_lab/scratch/ichen/projects"
if _COFOLDING_EXPERIMENT_PATH not in sys.path:
    sys.path.append(_COFOLDING_EXPERIMENT_PATH)

_RESCORE_DB_PATH = "/lustre/fs6/lyu_lab/scratch/ichen/projects/rescore/boltz2_rescore_database/src"
if _RESCORE_DB_PATH not in sys.path:
    sys.path.append(_RESCORE_DB_PATH)

_RESCORE_INPUT_PATH = "/lustre/fs6/lyu_lab/scratch/ichen/projects/rescore/boltz2_rescore_input/src"
if _RESCORE_INPUT_PATH not in sys.path:
    sys.path.append(_RESCORE_INPUT_PATH)

from boltz2_rescore_database.data_paths.dudez import (
    protein_info_path,
    msa_path,
    receptor_id_path,
    ligand_smiles_from_mol_path
)
from cofolding_analysis.utils.pyspark_df.set_up import (FilterPysparkData,
                                                        JoinPysparkData,
                                                        SetupAnalysis)
from boltz2_rescore_input.src.utils.batch import Batch

input_dir = "/lustre/fs6/lyu_lab/scratch/ichen/project_data/rescore/dudez_inputs"

spark = SparkSession.builder.appName("AF3_database").getOrCreate()
setup_analysis = SetupAnalysis(
    spark=spark,
    datapath_list={
        "protein_info": protein_info_path,
        "receptors": receptor_id_path,
        "msa": msa_path,
        "ligand_smiles":ligand_smiles_from_mol_path
    },
)
setup_analysis.set_globals_in_calling_module(globals())

protein_seqs = protein_info.join(
    receptors,
    on="recp_id",
    how="inner")
protein_seqs = protein_seqs.join(
    msa,
    on=["recp_id", "chain"],
    how="left"
)

def build_protein_dict(one_protein_pyspark, msa=True):

    protein_rows = one_protein_pyspark.collect()
    protein_list = []
    for row in protein_rows:
        sequence = row['seq']
        chain = row['chain']

        protein_dict = {"protein":{
            "id": chain,
            "sequence": sequence,
        }}

        if msa:
            protein_dict["protein"]["msa"] = row["msa_path"]
        protein_list.append(protein_dict)
    return protein_list

import string
idx_to_chain = {i: ch for i, ch in enumerate(string.ascii_uppercase)}

def build_ligand_list(smiles, protein_count):
    ligand_list = [{
        "ligand": {
            "id": idx_to_chain[protein_count],
            "smiles": smiles
        }
    }]
    return ligand_list, idx_to_chain[protein_count]

def build_property(alpha):
    return {
        "affinity": {
            "binder": alpha
        }
    }

def build_boltz2_config(one_protein_pyspark, smiles,msa):
    boltz_config = {
        "version": 1,
        "sequences": [],
        "properties": []
    }
    protein_list = build_protein_dict(one_protein_pyspark, msa)
    ligand_list, alpha = build_ligand_list(smiles, len(protein_list))
    boltz_config["sequences"] += protein_list
    boltz_config["sequences"] += ligand_list
    boltz_config["properties"].append(build_property(alpha))

    return boltz_config

recp_ids = [row["recp_id"] for row in receptors.select("recp_id").distinct().collect()]
receptor_mapping = {
        row["recp_id"]: row["recp_name"] for row in receptors.collect()
    }

for rid in recp_ids:
    one_protein = protein_seqs.filter(protein_seqs.recp_id == rid)
    one_protein = one_protein.orderBy(asc("chain"))
    
    ligand_smiles_rows = ligand_smiles.filter(ligand_smiles.recp_id == rid).collect()

    for row in ligand_smiles_rows:
        smiles = row['smiles']
        compound_id = row['compound_id']

        config_file = build_boltz2_config(one_protein, smiles, msa=True)
        recp_dir = f"{input_dir}/{receptor_mapping[rid]}"
        os.makedirs(recp_dir, exist_ok=True)
        yaml_file = f"{recp_dir}/{compound_id}.yaml"
        Batch.write_yaml_line_by_line(yaml_file, config_file)
