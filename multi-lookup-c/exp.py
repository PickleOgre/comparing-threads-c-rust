import os, subprocess, statistics, csv, math

ERR_THRESHOLD = 0.1
PROGRAM = "./multi-lookup"
SIZES = [100, 250, 500]
ZC = 1.96
DEBUG = True

def findError(zc, std, n):
  return (zc * std) / math.sqrt(n)

if not os.path.exists(PROGRAM):
    subprocess.run(["make"], check=True)

for size in SIZES: # Warmup cache
    subprocess.run([PROGRAM, str(size), "results.txt"], capture_output=True, text=True)

with open("results.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["N", "time_µs"])
    if DEBUG: print("size\tn\tmean\tstdev\tME")
    for s in SIZES:
        times = []
        input_arg = "input/" + str(s) + "names.txt"
        n = 0
        while n < 100 or findError(ZC, statistics.stdev(times), n) > ERR_THRESHOLD * statistics.mean(times):
            out = subprocess.run([PROGRAM, input_arg, "results.txt"], capture_output=True, text=True)
            time = int(out.stdout.strip())
            writer.writerow([s, time])
            times.append(time)
            n+=1
            if n >= 1000: break
        if DEBUG:
            stdev = statistics.stdev(times)
            print(str(s) + "\t" + str(n) + "\t" + str(statistics.mean(times)) + "\t" + str(stdev) + "\t" + str(findError(ZC, stdev, n)))
