#! /bin/bash

time python run_alphafold.py \
   --input_dir=/root/af_input \
   --model_dir=/root/models \
   --output_dir=/root/af_output

echo "Done!"

