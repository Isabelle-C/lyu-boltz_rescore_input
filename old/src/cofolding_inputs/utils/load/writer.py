import os

from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord


def save_as_fasta(
    protein_seq: str,
    ligand_letter: str,
    molecule_smiles: str,
    output_fasta: str,
    msa_filepath: str,
):

    if os.path.exists(output_fasta):
        print(f"{output_fasta} already exists. Skipping...")
        return

    if molecule_smiles is not None:

        if msa_filepath is not None:
            records = []
            for k, v in protein_seq.items():
                records.append(
                    SeqRecord(Seq(v), id=f"{k}|protein|{msa_filepath}", description="")
                )

            records.append(
                SeqRecord(
                    Seq(molecule_smiles), id=f"{ligand_letter}|smiles", description=""
                )
            )

        else:
            records = []
            for k, v in protein_seq.items():
                records.append(SeqRecord(Seq(v), id=f"{k}|protein", description=""))
            records.append(
                SeqRecord(
                    Seq(molecule_smiles), id=f"{ligand_letter}|smiles", description=""
                )
            )

        SeqIO.write(records, output_fasta, "fasta")

    else:
        print("Not saving file")
