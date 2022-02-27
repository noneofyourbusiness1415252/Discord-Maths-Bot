#include <math.h>
#include <stdlib.h>
unsigned *primesupto(unsigned, unsigned *);
unsigned *primesupto(unsigned n, unsigned *total) {
	unsigned corr = 2 - (n % 6 > 1), *primes = NULL;
	n = n - n % 6 + 6;
	unsigned thn = n / 3;
	_Bool *sieve = calloc(thn, 1);
	for (unsigned i = 1; i <= sqrt(n) / 3; i++)
		if (!sieve[i]) {
			unsigned k = 3 * i + 1 | 1;
			for (unsigned j = k * k / 3; j < thn; j += 2 * k) sieve[j] = 1;
			for (unsigned j = k * (k - 2 * (i & 1) + 4) / 3; j < thn; j += 2 * k)
				sieve[j] = 1;
		}
	for (unsigned i = thn - corr; i > 0; i--)
		if (!sieve[i]) {
			primes = realloc(primes, ++*total * 4);
			primes[*total - 1] = 3 * i + 1 | 1;
		}
	free(sieve);
	primes = realloc(primes, *total * 4 + 8);
	primes[(*total)++] = 3;
	primes[(*total)++] = 2;
	return primes;
}
