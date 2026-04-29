/*
 * File: monte-carlo-c
 * Author: Josiah Lawrence
 * Project: CSCI 440 Final
 * Create Date: 2026/04/26
 * Description:
 *  This is a threaded implementation of a
 *  monte carlo estimation of pi.
 *
 */

#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <unistd.h>

#define NUM_THREADS 10
#define MINARGS 2
#define USAGE "<number of samples>"

typedef struct
{
  long n_samples;
  long hits;
  unsigned int seed;
} ThreadArgs;

/* Function for each thread to run */
void*
sample(void* arg)
{
  ThreadArgs* args = (ThreadArgs*)arg;
  long hits = 0;
  for (long i = 0; i < args->n_samples; i++) {
    double x = (double)rand_r(&args->seed) / RAND_MAX;
    double y = (double)rand_r(&args->seed) / RAND_MAX;
    if (x * x + y * y <= 1.0) {
      hits++;
    }
  }

  args->hits = hits;
  return NULL;
}

int
main(int argc, char* argv[])
{
  /* Check Arguments */
  if (argc < MINARGS) {
    fprintf(stderr, "Not enough arguments: %d\n", (argc - 1));
    fprintf(stderr, "Usage:\n %s %s\n", argv[0], USAGE);
    return EXIT_FAILURE;
  };

  /* Setup Local Vars */
  pthread_t threads[NUM_THREADS];
  ThreadArgs args[NUM_THREADS];
  int rc;
  long t;
  long total_samples = atol(argv[1]);
  long chunk = total_samples / NUM_THREADS;

  /* Start timer */
  struct timeval begin, end;
  gettimeofday(&begin, 0);

  /* Spawn threads */
  for (t = 0; t < NUM_THREADS; t++) {
    args[t] = (ThreadArgs){
      .n_samples = (t == NUM_THREADS - 1) ? total_samples - t * chunk : chunk,
      .hits = 0,
      .seed = (unsigned int)t + 1,
    };
    rc = pthread_create(&threads[t], NULL, sample, &args[t]);
    if (rc) {
      fprintf(stderr, "ERROR; return code from pthread_create() is %d\n", rc);
      exit(EXIT_FAILURE);
    }
  }

  /* Wait for All Threads to Finish */
  for (t = 0; t < NUM_THREADS; t++) {
    pthread_join(threads[t], NULL);
  }

  /* Collect results */
  long total_hits = 0;
  for (t = 0; t < NUM_THREADS; t++) {
    total_hits += args[t].hits;
  }

  /* Stop timer and print elapsed time */
  gettimeofday(&end, 0);
  long seconds = end.tv_sec - begin.tv_sec;
  long microseconds = end.tv_usec - begin.tv_usec;
  printf("%ld\n", seconds * 1000000 + microseconds);

  /* Calculate and print estimation of pi */
  double pi = 4.0 * total_hits / total_samples;
  fprintf(stderr, "pi = %f\n", pi);

  return 0;
}
