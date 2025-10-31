import os
import random
import shutil

# Paths
home_dir = "/lustre/fs6/lyu_lab/scratch/kmenon01/af3/testing/known_lig_cofold"   # change to absolute path if needed
dest_dir = "/lustre/fs6/lyu_lab/scratch/ichen/collected_jsons"
os.makedirs(dest_dir, exist_ok=True)

# Iterate over subfolders inside home_dir
for subfolder in ['ampc','d4','sigma']:
    sub_path = os.path.join(home_dir, subfolder)
    if not os.path.isdir(sub_path):
        continue  # skip non-directories
    
    output_dir = os.path.join(sub_path, "output")
    if not os.path.isdir(output_dir):
        continue
    
    # Pick a random folder inside "output"
    candidates = [d for d in os.listdir(output_dir) if os.path.isdir(os.path.join(output_dir, d))]
    if not candidates:
        continue
    
    chosen = random.choice(candidates)
    chosen_lower = chosen.lower()
    
    # Build json file path
    json_path = os.path.join(
        output_dir, chosen, "af_output", chosen_lower, f"{chosen_lower}_data.json"
    )
    
    if not os.path.isfile(json_path):
        print(f"⚠️ File not found for {subfolder}: {json_path}")
        continue
    
    # Copy and rename
    dest_file = os.path.join(dest_dir, f"{subfolder}.json")
    shutil.copy(json_path, dest_file)
    print(f"✅ Copied {json_path} → {dest_file}")
