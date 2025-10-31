
import os
import shutil

recp_name = 'ABL1'

new_output_dir = f'/lustre/fs6/lyu_lab/scratch/ichen/data/15_dudez_af3/af_remaining/{recp_name}/af_output_done'
new_input_dir = f'/lustre/fs6/lyu_lab/scratch/ichen/data/15_dudez_af3/af_remaining/{recp_name}/af_inputs_done'
os.makedirs(new_output_dir, exist_ok=True)
os.makedirs(new_input_dir, exist_ok=True)


for i in os.listdir(f'/lustre/fs6/lyu_lab/scratch/ichen/data/15_dudez_af3/af_remaining/{recp_name}/af_output'):
    shutil.move(f"/lustre/fs6/lyu_lab/scratch/ichen/data/15_dudez_af3/af_remaining/{recp_name}/af_inputs/{i.upper()}.json", f"{new_input_dir}/{i.upper()}.json")
    shutil.move(f'/lustre/fs6/lyu_lab/scratch/ichen/data/15_dudez_af3/af_remaining/{recp_name}/af_output/{i}', f"{new_output_dir}/{i}")
