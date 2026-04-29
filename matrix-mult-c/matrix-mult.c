/*
 * File: matrix-mult-c
 * Author: Josiah Lawrence
 * Project: CSCI 440 Final
 * Create Date: 2026/04/26
 * Description:
 *  This is a threaded implementation of a
 *  matrix multiplication program.
 *
 */

#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <unistd.h>

#define NUM_THREADS 10
#define MINARGS 2
#define USAGE "<matrix size>"

typedef struct
{
  void *A, *B, *C;
  int N, start_row, end_row;
} ThreadArgs;

/* Function for each thread to run */
void*
multiplyRows(void* arg)
{
  /* Cast void args back into their types */
  ThreadArgs* args = (ThreadArgs*)arg;
  int N = args->N;
  double (*A)[N] = (double (*)[N])args->A;
  double (*B)[N] = (double (*)[N])args->B;
  double (*C)[N] = (double (*)[N])args->C;

  for (int row = args->start_row; row < args->end_row; row++) {
    for (int j = 0; j < N; j++) {
      double sum = 0.0;
      for (int k = 0; k < N; k++)
        sum += A[row][k] * B[k][j];
      C[row][j] = sum;
    }
  }

  /* Exit, returning NULL*/
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
  int N = atoi(argv[1]);

  /* Define and initialize arrays */
  double (*A)[N] = malloc(N * sizeof(*A));
  double (*B)[N] = malloc(N * sizeof(*B));
  double (*C)[N] = calloc(N, sizeof(*C));

  for (int i = 0; i < N; i++) {
    for (int j = 0; j < N; j++) {
      A[i][j] = (double)(i + j);
      B[i][j] = (double)(i * j);
    }
  }

  /* Start timer */
  struct timeval begin, end;
  gettimeofday(&begin, 0);

  /* Spawn threads */
  for (t = 0; t < NUM_THREADS; t++) {
    int chunk = N / NUM_THREADS;
    args[t] = (ThreadArgs){
      .A = A,
      .B = B,
      .C = C,
      .N = N,
      .start_row = t * chunk,
      .end_row = (t == NUM_THREADS - 1) ? N : (t + 1) * chunk,
    };
    rc = pthread_create(&(threads[t]), NULL, multiplyRows, &args[t]);
    if (rc) {
      fprintf(stderr, "ERROR; return code from pthread_create() is %d\n", rc);
      exit(EXIT_FAILURE);
    }
  }

  /* Wait for All Threads to Finish */
  for (t = 0; t < NUM_THREADS; t++) {
    pthread_join(threads[t], NULL);
  }

  /* Stop timer and print elapsed time */
  gettimeofday(&end, 0);
  long seconds = end.tv_sec - begin.tv_sec;
  long microseconds = end.tv_usec - begin.tv_usec;
  printf("%ld\n", seconds * 1000000 + microseconds);;

  free(A);
  free(B);
  free(C);
  return 0;
}
