import os, subprocess, statistics, csv, math

ERR_THRESHOLD = 0.1
PROGRAM = "./multi-lookup"
SIZES = [100, 250, 500]
ZC = 1.96
DEBUG = True
WARMUP_RUNS = 16

def findError(zc, std, n):
  return (zc * std) / math.sqrt(n)

if not os.path.exists(PROGRAM):
    subprocess.run(["make"], check=True)    

with open("results.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["size", "time_µs"])
    if DEBUG: print("size\tn\tmean\tstdev\tME")
    for s in SIZES:
        input_arg = "input/" + str(s) + "names.txt"
        i = 0
        while i < WARMUP_RUNS: # Warmup cache
            subprocess.run([PROGRAM, input_arg, "results.txt"], capture_output=True, text=True)
            i+= 1
        times = []
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
