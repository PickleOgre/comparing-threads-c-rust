# This script runs an experiment script inside each program folder, 
# then creates graphs based on the results.csv files.

import subprocess, sys, math
import pandas as pd
import matplotlib.pyplot as plt

USAGE = "python run_experiments.py <mode>"
MODES = ["all", "run", "graph"]
ZC = 1.96 # Critical value

def findError(zc, std, n):
  return (zc * std) / math.sqrt(n)

mode = "all"
if len(sys.argv) > 1:
  mode = sys.argv[1]
  if mode not in ["all", "run", "graph"]:
    print("Usage: " + USAGE);
    print("Modes: " + str(MODES))

# Experiment Directory Paths
programs = [
  "matrix-mult-c",
  "matrix-mult-rust",
  "monte-carlo-c",
  "monte-carlo-rust",
  "multi-lookup-c",
  "multi-lookup-rust"
]

# CSV File Paths
matrix_mult_c_csv = "./matrix-mult-c/results.csv"
matrix_mult_rust_csv = "./matrix-mult-rust/results.csv"
monte_carlo_c_csv = "./monte-carlo-c/results.csv"
monte_carlo_rust_csv = "./monte-carlo-rust/results.csv"
multi_lookup_c_csv = "./multi-lookup-c/results.csv"
multi_lookup_rust_csv = "./multi-lookup-rust/results.csv"

# Run each experiment, one at a time
if mode in ["all", "run"]:
  for p in programs:
    print("Running "+p+"...")
    subprocess.run(["python3", "exp.py"], cwd="./"+p, check=True)

# Graph results
if mode in ["all", "graph"]:
  for p in programs:
    print(p)
    df = pd.read_csv("./"+p+"/results.csv")
    grouped = [group["time_µs"].values for _, group in df.groupby("N")]
    labels = df["N"].unique()
    print(df.groupby("N")["time_µs"].std())

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.boxplot(grouped, tick_labels=labels)
    ax.set_xlabel("N")
    ax.set_ylabel("Execution time (µs)")
    if "multi-lookup" in p:
      ax.set_yscale("log")

    plt.tight_layout()
    plt.savefig(p+"-plot.png")
