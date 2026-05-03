# This script runs an experiment script inside each program folder, 
# then creates graphs based on the results.csv files.

import subprocess, statistics, csv
import pandas as pd
import matplotlib.pyplot as plt

# Binary Paths
matrix_mult_c_bin = "./matrix-mult-c/matrix-mult"
matrix_mult_rust_bin = "./matrix-mult-rust/target/release/matrix-mult-rust"
monte_carlo_c_bin = "./monte-carlo-c/monte-carlo"
monte_carlo_rust_bin = "./monte-carlo-rust/target/release/monte-carlo-rust"
multi_lookup_c_bin = "./multi-lookup-c/multi-lookup"
multi_lookup_rust_bin = "./multi-lookup-rust/target/release/multi-lookup-rust"

# Experiment Directory Paths
exp_dirs = [
  "./matrix-mult-c",
  "./matrix-mult-rust",
  "./monte-carlo-c",
  "./monte-carlo-rust",
  "./multi-lookup-c",
  "./multi-lookup-rust"
]

# CSV File Paths
matrix_mult_c_csv = "./matrix-mult-c/results.csv"
matrix_mult_rust_csv = "./matrix-mult-rust/results.csv"
monte_carlo_c_csv = "./monte-carlo-c/results.csv"
monte_carlo_rust_csv = "./monte-carlo-rust/results.csv"
multi_lookup_c_csv = "./multi-lookup-c/results.csv"
multi_lookup_rust_csv = "./multi-lookup-rust/results.csv"

# Run each experiment, one at a time
for d in exp_dirs:
  subprocess.run(["python3", "exp.py"], cwd=d, check=True)
