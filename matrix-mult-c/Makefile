CC = gcc
CFLAGS = -c -02 -Wall -Wextra
LFLAGS = -O2 -Wall -Wextra -pthread

.PHONY: all clean

all: matrix-mult

matrix-mult: matrix-mult.c
	$(CC) $(LFLAGS) $^ -o $@

clean:
	rm -f matrix-mult results.csv
	rm -f *.o
	rm -f *~
