CC = gcc
CFLAGS = -c -02 -Wall -Wextra
LFLAGS = -O2 -Wall -Wextra -pthread

.PHONY: all clean

all: monte-carlo

monte-carlo: monte-carlo.c
	$(CC) $(LFLAGS) $^ -o $@

clean:
	rm -f monte-carlo results.csv
	rm -f *.o
	rm -f *~
