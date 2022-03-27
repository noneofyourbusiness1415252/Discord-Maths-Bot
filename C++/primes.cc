#include <cmath>
#include <cstdio>
#include <cstdlib>
int main(int, char **argv) {
	printf("2");
	unsigned limit = atoi(argv[1]), half = limit / 2, total = 1,
			 isqrt = sqrt(limit);
	auto sieve = new bool[half]();
	for (auto i = 3u; i <= isqrt; i += 2)
		if (!sieve[i / 2])
			for (auto j = i * i / 2; j < half; j += i) sieve[j] = true;
	for (auto i = 1u; i < half; i++)
		if (!sieve[i]) {
			printf(", %u", 2 * i + 1);
			total++;
		}
	printf("\nTotal: %u\n", total);
}