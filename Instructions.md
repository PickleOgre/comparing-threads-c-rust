# CSCI440 Inquiry Based Final Project

## Goals
This project has the following goals:

* Student sets out to answer a question about a topic related to Operating Systems. 
* Student devises a way to test and/or gain understanding about the question they are trying to ask through a hands-on implementation of the concept.
	* Should come up with a procedure or method for testing the effectiveness of known solutions or their solutions.
* Student writes up a document with their findings.


## Sample Questions
Recommended questions are shown below; these are pre-approved. If you are interested in answering a different question, you need to get approval first by emailing me with your question and describing how you plan to test it:

* How does the performance of threads in C compare to one of the following languages?
	* Python (multi-process)
	* Rust
	* Go
	* Java
	* Other (get approval)
* What file system performs best for small files on Linux? Or alternatively what about for large files? (using `dd` for benchmarks, do not use IOzone or bonnie++) 
	* Consider at least 5 of the following filesystems:
		* ext4
		* ext2
		* xfs
		* FAT32
		* ZFS
		* BTRFS
		* NTFS (might be CIFS under linux)
* How does the performance of differing IPC mechanisms compare in C to one of the following languages?
	* Python
	* Rust
	* Go
	* Java
	* Other (get approval)


Extra Credit question (this is not an alternative to one of the above questions; this must be answered in addition to answering one of the questions above): 
* (EC) How much does Docker virtualization impact the performance of threads compared to a native (or native VM) system in one of the following languages?
	* C
	* Python
	* Rust
	* Go
	* Java
	* Other (get approval)


Answering any of these questions will require several components, including:

* Identify a Metric
	* Determine what you will be comparing, e.g. the execution time for a specific task
* Design an Experiment
	* For comparing performance of threads, choose computationally intensive tasks that are easily parallelizable (CPU intensive, not I/O intensive) such as: DNS (Domain Name System) Resolution, Matrix Multiplication, Monte Carlo (estimation of pi)
 		* Change the amount of data being passed to the programs, not the number of threads -- choose a number of threads (more than 1), and test each program with this number of threads. For the amount of data, change (for example) the number of names being resolved, the size of the matrix, or the number of points generated (test each program with at least 3 different amounts of data).
 	* For comparing file systems, compare reads and writes on files of different sizes with different block sizes for each file (use at least 3 different file sizes and at least 3 different block sizes for each file)
 	* Comparing performance of IPC methods will be similar to comparing threads -- you will need to choose a few computationally intensive tasks to compare.
  		* Choose a method, e.g. pipes, message queues, shared memory, or local sockets, and implement this method across each program. You should be comparing different amounts of data with each program.
* Testing Procedure and Data Collection
	* You will need to run the workload multiple times for each test case to account for noise, caching effects, and other statistical variance. Consider your margin of error when determining how many times you need to run each workload.
 	* If you only run 1 or a couple tests, any results you get could be misleading. To get a meaningful result, you need a large enough sample size and conditions that are as consistent as possible. 
* Test Results and Quantitative Analysis
	* Calculate your key performance indicators and interpret your results.
 		* e.g. consider the mean average execution time and range of execution times
   		* It may help to visualize your results with one or more charts or graphs.  
 	* Determine if there are any statistically significant differences.
    * Consider if any operating systems concepts can help explain your results (what factors influence performance?)
    * Your answer to your project question should be based on the evidence presented in the report.

## Evaluation

Your project will be graded based on the following components.

* Paper - You will submit a short paper describing the following:
	* Your Approved Question
		* What is your question?
   		* When describing your question, make sure to define the workload, including any applicable details. For example:
     		* If comparing performance, what languages did you compare, and what algorithms did you implement?
       		* If comparing file systems, which file systems did you compare? Make sure you are using an approved question and approved languages or file systems.
	* Your Experimental Setup
		* Describe the environment where you are completing your testing, including details about your machine configuration such as the amount of CPUs and memory, operating system type and image, etc.
   		* Are there any side effects or artifacts related to your experimental setup that might impact your results? You should explain any ways that you have minimized noise in your setup that could distort your results.
	* Your Testing Procedure
  		* How did you run your tests to answer your question?
    	* Some things you should be considering in describing your testing procedure: How did you collect your data? To measure performance, what did you use to time your programs?
	* Your Test Results
		* Provide your actual test results, e.g. the mean average and standard deviation of your execution times.
   		* How accurate are your results? 
			* How many tests did you run for each case? Make sure you run enough tests that your results are sufficiently robust. It is not uncommon to run 30+ tests for each program.
   			* What was your [margin of error](https://en.wikipedia.org/wiki/Margin_of_error)? There is not one perfect margin of error that should be used in all cases, but for this project, an acceptable goal is to aim for a margin of error around 5-10%.
      		* What z-score did you use for your confidence value? 
		* How did you make sure to have enough variation in your test code? 
			* If comparing the performance of different programming languages, it is expected that you test with multiple computationally intensive algorithms/programs (at least 3). Some examples of programs you might implement include DNS threads, matrix multiplication threads, the Monte Carlo method for calculating pi with threads, or other threaded applications.
			* If comparing the performance of different file systems, it is expected that you include variations in block and file sizes (at minimum, 3 different file sizes and 3 different block sizes for each file size). Make sure you have also defined what you consider a small (or large) file.
			* If comparing the performance of differing IPC mechanisms, it is expected that you include variation in the size of communication data sent via IPC.
	* Your Conclusion/Answer To The Question
  		* Based on your test results, how does the performance compare? Was there a statistically significant difference? How should your results be interpreted?
	* Your Learning Outcome
  		* What did you learn from answering the question and completing this inquiry-based project? You can consider what you learned while setting up your experiment, implementing the programs, doing the testing, interpreting the results, researching, etc.
* Code - You must submit the code for your project along with the paper submission.
	* Include all of your source code and any scripts, Makefiles, etc used to compile and run your code.
 	* You do not need to include compiled code, build output directories, files generated at runtime, and other files commonly ignored in a git repo.
* References - You must clearly reference any resources or source code you used or adapted. References may be included in your code or in a separate document or subfolder.
	* Include a link (at minimum) to any internet content you have referenced.
	* If you use Large Language Models (LLMs) and other AI tools, you must cite them. Make sure to include your prompt(s) and details about the AI tool. You may include a link to the full transcript or include it in an appendix. Here are some examples:
 		* [How to cite ChatGPT](https://apastyle.apa.org/blog/how-to-cite-chatgpt) (APA style)
   		* [How do I cite generative AI in MLA style?](https://style.mla.org/citing-generative-ai/) (MLA style)

## Project Submission

You will submit a tar.gz to INGInious system. The tar.gz should have the following:

* PDF of your paper that discusses your results, analysis, motivation, conclusions, etc. 
* All of the code for you used for your project. 
	* Alternatively you can add me to a repository with all your code for the project, and just put a README in the tar.gz with the link to this repository.
 * All references should be included in your tar.gz submission.
 	* References may be included in your code, in a README.md file, or in a dedicated directory within your project.
 	
	
## Extra Credit

You can get up to 10 points of extra credit for every additional question you answer. 
