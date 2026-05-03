import os, subprocess, statistics, csv

program = "./target/release/multi-lookup"
if not os.path.exists(program):
    subprocess.run(["cargo", "build", "--release"], check=True)
sizes = [100, 250, 500, 750, 1000, 1500, 2000]
runs = 1

with open("results.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["N", "mean_µs", "min_µs", "max_µs"])

    for n in sizes:
        times = []
        input_arg = "input/" + str(n) + "names.txt"
        for _ in range(runs):
            out = subprocess.run([program, input_arg, "output.txt"], capture_output=True, text=True)
            times.append(float(out.stdout.strip()))
        writer.writerow([n, statistics.mean(times), min(times), max(times)])
