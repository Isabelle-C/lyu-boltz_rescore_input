#!/bin/bash

for pdb in ./*.pdb; do
    [ -e "$pdb" ] || continue  # skip if no pdb files
    base="${pdb%.pdb}"
    obabel "$pdb" -O "${base}.mol2"
    if [ $? -eq 0 ] && [ -f "${base}.mol2" ]; then
        rm "$pdb"
        echo "Converted and removed $pdb"
    else
        echo "Failed to convert $pdb"
    fi
done

# input_dir="/lustre/fs6/lyu_lab/scratch/ichen/data/boltz_runs/ampc_pdb"
# output_dir="/lustre/fs6/lyu_lab/scratch/ichen/data/boltz_runs/ampc_mol2"

# mkdir -p "$output_dir"

# for pdb in "$input_dir"/*.pdb; do
#     base=$(basename "$pdb" .pdb)
#     obabel "$pdb" -O "$output_dir/$base.mol2"
# done