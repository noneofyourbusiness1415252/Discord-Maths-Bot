#include <cmath>
#include <iostream>
#include <string>
using namespace std;
int main(int, char **argv) {
	ios_base::sync_with_stdio(false);
	cout << 2;
	unsigned limit = stoi(argv[1]), half = limit / 2, total = 1,
			 isqrt = sqrt(limit);
	auto sieve = new bool[half]();
	for (unsigned i = 3; i <= isqrt; i += 2)
		if (!sieve[i / 2])
			for (unsigned j = i * i / 2; j < half; j += i) sieve[j] = true;
	for (unsigned i = 1; i < half; i++)
		if (!sieve[i]) {
			cout << ", " << 2 * i + 1;
			total++;
		}
	cout << "\nTotal: " << total << '\n';
}