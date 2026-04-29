import subprocess, statistics, csv

program = "./monte-carlo"
sizes = [100, 250, 500, 750, 1000, 1500, 2000, 5000, 10000, 20000]
runs = 20

with open("results.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["N", "mean_µs", "min_µs", "max_µs"])
    for n in sizes:
        times = []
        for _ in range(runs):
            out = subprocess.run([program, str(n)], capture_output=True, text=True)
            times.append(int(out.stdout.strip()))
        writer.writerow([n, statistics.mean(times), min(times), max(times)])
