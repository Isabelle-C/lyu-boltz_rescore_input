import pandas as pd
from rcsbapi.data import DataQuery as Query

ligands_data_path = (
    "/ru-auth/local/home/ichen/lyu_scratch/rescore/input/af3/pdb_dudez/xtal_lig.csv"
)
ligands_data = pd.read_csv(ligands_data_path)

receptor_name = []
ligand_name = []
smiles_data = []
for index, row in ligands_data.iterrows():
    xtal_name = row["xtal_name"]
    recp_name = row["recp_name"]

    print(f"Processing {xtal_name} for receptor {recp_name}")
    # Query to get chemical descriptors including SMILES
    try:
        query = Query(
            input_type="chem_comps",
            input_ids=[xtal_name],
            return_data_list=[
                "chem_comps.rcsb_id",
                "chem_comps.pdbx_chem_comp_descriptor",
            ],
        )
        result = query.exec()

        if result and "data" in result and "chem_comps" in result["data"]:
            chem_comp = result["data"]["chem_comps"][0]
            comp_id = chem_comp.get("rcsb_id", "Unknown")
            descriptors = chem_comp.get("pdbx_chem_comp_descriptor", [])

            print(f"Chemical Component: {comp_id}")
            print("\nSMILES_CANONICAL entries:")
            print("-" * 50)

            canonical_smiles = []
            for desc in descriptors:
                if desc.get("type") == "SMILES_CANONICAL":
                    program = desc.get("program", "Unknown")
                    version = desc.get("program_version", "Unknown")
                    smiles = desc.get("descriptor", "")

                    print(f"Program: {program} (v{version})")
                    print(f"SMILES: {smiles}")
                    print()

                    canonical_smiles.append({"program": program, "smiles": smiles})

            # # Also show all SMILES (not just canonical) for comparison
            # print("\nAll SMILES entries:")
            # print("-" * 50)
            # for desc in descriptors:
            #     if desc.get('type') in ['SMILES', 'SMILES_CANONICAL']:
            #         program = desc.get('program', 'Unknown')
            #         smiles_type = desc.get('type')
            #         smiles = desc.get('descriptor', '')
            #         print(f"{smiles_type} ({program}): {smiles}")

            # print(f"\nFound {len(canonical_smiles)} SMILES_CANONICAL entries")

        else:
            print("No data found")

        receptor_name.append(recp_name)
        ligand_name.append(xtal_name)
        smiles_data.append(canonical_smiles)

    except Exception as e:
        print(f"Query failed: {e}")

CACTVS_list = []
openeye_list = []
for i in smiles_data:
    for j in i:
        if j["program"] == "CACTVS":
            CACTVS_list.append(j["smiles"])
        elif j["program"] == "OpenEye OEToolkits":
            openeye_list.append(j["smiles"])

data = {
    "recp_name": receptor_name,
    "ligand_name": ligand_name,
    "CACTVS": CACTVS_list,
    "OpenEye OEToolkits": openeye_list,
}
df = pd.DataFrame(data)
df.to_csv(
    "/ru-auth/local/home/ichen/lyu_scratch/rescore/input/af3/pdb_dudez/completed_smiles.csv"
)
