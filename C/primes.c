#include <math.h>
#include <stdio.h>
#include <stdlib.h>
int main(int argc, char **argv) {
	printf("2");
	unsigned limit = atoi(argv[1]), half = limit / 2, total = 1, isqrt = sqrt(limit);
	_Bool *sieve = malloc(half);
	for (unsigned i = 3; i <= isqrt; i += 2)
		if (!sieve[i / 2])
			for (unsigned j = i * i / 2; j < half; j += i) sieve[j] = 1;
	for (unsigned i = 1; i < half; i++)
		if (!sieve[i]) {
			printf(", %d", 2 * i + 1);
			total++;
		}
	printf("\nTotal: %d\n", total);
}