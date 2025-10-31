import sys
from pathlib import Path
import pprint
import random
import time
import zipfile
from pyspark.sql import SparkSession
from pyspark.sql.functions import asc
from pyspark import SparkContext, SparkFiles

import string
## --- Path setup ---
msa_src = Path("/lustre/fs6/lyu_lab/scratch/ichen/projects/rescore/msa_pulling/src")
msa_pkg = msa_src / "msa_pulling"
zip_path = msa_src.parent / "msa_pulling.zip"

# --- Create zip from the *src* directory ---
if not zip_path.exists():
    with zipfile.ZipFile(zip_path, "w") as zf:
        for f in msa_pkg.rglob("*"):
            zf.write(f, f.relative_to(msa_src))  # relative to src

# --- Make driver aware ---
if str(msa_src) not in sys.path:
    sys.path.insert(0, str(msa_src))

# --- Ship to executors ---
sc = SparkContext.getOrCreate()
sc.addPyFile(str(zip_path))

from msa_pulling.main import compute_msa

_COFOLDING_PATH = "/lustre/fs6/lyu_lab/scratch/ichen/projects/cofolding_analysis/src"
if _COFOLDING_PATH not in sys.path:
    sys.path.append(_COFOLDING_PATH)


_RESCORE_DB_PATH = "/lustre/fs6/lyu_lab/scratch/ichen/projects/rescore/boltz2_rescore_database/src"
if _RESCORE_DB_PATH not in sys.path:
    sys.path.append(_RESCORE_DB_PATH)

import os
os.environ["MMSEQS_THREADS"] = "4"

from boltz2_rescore_database.data_paths.dudez import (
    protein_info_path,
    receptor_id_path,
    config_receptors,
)
from cofolding_analysis.utils.pyspark_df.set_up import (FilterPysparkData,
                                                        JoinPysparkData,
                                                        SetupAnalysis)



n_cpus = int(os.getenv("SLURM_CPUS_PER_TASK", os.cpu_count()))
print(f"{n_cpus} CPUs allocated by Slurm.")

python_bin = "/lustre/fs6/lyu_lab/scratch/ichen/py_envs/cofolding_analysis/bin/python"

os.environ["PYSPARK_PYTHON"] = python_bin
os.environ["PYSPARK_DRIVER_PYTHON"] = python_bin

def check_python_versions(spark):
    import platform
    driver_version = platform.python_version()
    print(f"[Driver Python] {driver_version}")

    def get_worker_version(_):
        import platform
        return platform.python_version()

    worker_versions = spark.sparkContext.parallelize(range(4), 4).map(get_worker_version).collect()
    print(f"[Worker Python] {worker_versions}")

def has_expected_csvs(save_dir: Path, seq_rows: list) -> bool:
    """
    Check whether the number of CSV files in the directory matches the number of sequence rows.
    """
    csv_count = len(list(save_dir.glob("*.csv")))
    expected = len(seq_rows)
    print(f"[{save_dir.name}] CSV count: {csv_count} / expected: {expected}")
    return csv_count == expected

def run_msa(args):
    """
    Each worker runs compute_msa() for one receptor.
    """
    recp_id, broadcast_mapping, seq_rows = args
    recp_name = broadcast_mapping.value[recp_id]

    # Save directory per receptor
    save_dir = Path(
        f"/lustre/fs6/lyu_lab/scratch/ichen/project_data/rescore/dudez_msa_1027/{recp_name}"
    )
    save_dir.mkdir(parents=True, exist_ok=True)

    if not has_expected_csvs(save_dir, seq_rows):
        time.sleep(random.uniform(0.5, 2.0))

        # Precompute mapping: {'A':0, 'B':1, ..., 'Z':25}
        chain_to_index = {ch: i for i, ch in enumerate(string.ascii_uppercase)}

        chain_dict = {
            f"{recp_name}_{chain_to_index.get(r['chain'].upper())}": r["seq"]
            for r in seq_rows
        }

        # Prepare chain dictionary directly from precollected data
        chain_dict = {f"{recp_name}_{i}": r["seq"] for i, r in enumerate(seq_rows)}
 
        print(f"Computing MSA for {recp_name}...")
        pprint.pprint(chain_dict)

        compute_msa(chain_dict,
            target_id=recp_name,
            msa_dir=save_dir,
            msa_server_url="https://api.colabfold.com",
            msa_pairing_strategy="greedy")
    
def main():

    spark = (
        SparkSession.builder
        .master(f"local[{n_cpus}]")
        .appName("MSA_Pipeline")
        .config("spark.driver.memory", "56g")
        .config("spark.local.dir", "/lustre/fs6/lyu_lab/scratch/$USER/spark_tmp")
        .config("spark.executorEnv.PYSPARK_PYTHON", python_bin)
        .config("spark.executorEnv.PYSPARK_DRIVER_PYTHON", python_bin)
        .config("spark.pyspark.driver.python", python_bin)
        .config("spark.pyspark.python", python_bin)
        .getOrCreate()
    )
    check_python_versions(spark)
    setup_analysis = SetupAnalysis(
        spark=spark,
        datapath_list={
            "protein_info": protein_info_path,
            "receptors": receptor_id_path,
        },
    )
    setup_analysis.set_globals_in_calling_module(globals())

    recp_ids = [row["recp_id"] for row in receptors.select("recp_id").distinct().collect()]

    receptor_mapping = {
        row["recp_id"]: row["recp_name"] for row in receptors.collect()
    }
    broadcast_mapping = spark.sparkContext.broadcast(receptor_mapping)

    # Collect protein sequences per receptor on driver
    protein_dict = (
        protein_info.join(receptors, on="recp_id", how="inner")
        .rdd
        .map(lambda r: (r["recp_id"], {"chain": r["chain"], "seq": r["seq"]}))
        .groupByKey()
        .mapValues(list)
        .collectAsMap()
    )

    args = [(rid, broadcast_mapping, protein_dict[rid]) for rid in recp_ids if rid in protein_dict]

    spark.sparkContext.parallelize(args, len(args)).foreach(run_msa)
    spark.stop()

if __name__ == "__main__":
    main()