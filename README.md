# Research Question
How does the time performance of threads in C compare to one of the following languages?

# Experimental Methods
---
## Metrics
- Execution time for a specific task
## Test Cases
- DNS Resolution
- Matrix multiplication
- Monte Carlo (estimation of pi)
## Variables
- Amount of data passed to the programs i.e. the number of names being resolved
## Analysis
- mean execution time 
- range of execution times


# Prep for Experiment
---
- Trim down both the C and Rust implementations for DNS resolution, and make sure they are as idiomatic and efficient as reasonably possible
- Prepare a C and Rust implementation for the second test case, i.e. Monte Carlo
- Set up a suitable environment for testing, i.e. a minimal Linux install on a spare drive on my desktop
- Make a Github repo with 4 folders, one for each test case and language, as well as all the testing code. Remember to never change the contents of the repo once it's published.