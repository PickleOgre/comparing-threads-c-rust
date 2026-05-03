import os, subprocess

# Experiment Directory Paths
exp_dirs = [
  "./matrix-mult-c",
  "./matrix-mult-rust",
  "./monte-carlo-c",
  "./monte-carlo-rust",
  "./multi-lookup-c",
  "./multi-lookup-rust"
]

# Clean generated files from all program directories
for d in exp_dirs:
  if "rust" in d:
    subprocess.run(["cargo", "clean"], cwd=d, check=True)
    if os.path.exists(d + "/results.csv"):
      subprocess.run(["rm", "results.csv"], cwd=d, check=True)
    if os.path.exists(d + "/output.txt"):
      subprocess.run(["rm", "output.txt"], cwd=d, check=True)
  else: 
    subprocess.run(["make", "clean"], cwd=d, check=True)
