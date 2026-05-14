import os, subprocess, statistics, csv, math

ERR_THRESHOLD = 0.05
PROGRAM = "./target/release/matrix-mult-rust"
SIZES = [100, 250, 500, 750, 1000, 1500, 2000]
ZC = 1.96
DEBUG = True

def findError(zc, std, n):
  return (zc * std) / math.sqrt(n)

if not os.path.exists(PROGRAM):
    subprocess.run(["cargo", "build", "--release"], check=True)

i = 0
while i < 3:
    subprocess.run([PROGRAM, str(SIZES[0])], capture_output=True, text=True) # Warmup
    i+=1

with open("results.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["size", "time_µs"])
    if DEBUG: print("size\tn\tmean\tstdev\tME")
    for s in SIZES:
        times = []
        n = 0
        while n < 3 or findError(ZC, statistics.stdev(times), n) > ERR_THRESHOLD * statistics.mean(times):
            out = subprocess.run([PROGRAM, str(s)], capture_output=True, text=True)
            time = int(out.stdout.strip())
            writer.writerow([s, time])
            times.append(time)
            n+=1
        if DEBUG:
            stdev = statistics.stdev(times)
            print(str(s) + "\t" + str(n) + "\t" + str(statistics.mean(times)) + "\t" + str(stdev) + "\t" + str(findError(ZC, stdev, n)))
