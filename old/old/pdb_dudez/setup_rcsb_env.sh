#!/bin/bash

# Script to create conda environment with rcsb-api

# Create a new conda environment named 'rcsb_env' with Python 3.9
echo "Creating conda environment 'rcsb_env'..."
conda create -n rcsb_env python=3.9 -y

# Activate the environment
echo "Activating environment..."
conda activate rcsb_env

# Install rcsb-api using pip
echo "Installing rcsb-api..."
pip install rcsb-api

# Also install some commonly needed packages
echo "Installing additional packages..."
pip install pandas numpy matplotlib jupyter

echo "Environment setup complete!"
echo "To activate the environment, run: conda activate rcsb_env"
echo "To test the installation, run your smiles2.py script"
python /ru-auth/local/home/ichen/lyu_scratch/rescore/pdb_dudez/smiles2.py