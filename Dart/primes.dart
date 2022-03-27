import "dart:math";
import "dart:io";
main(List args) {
	stdout.write(2);
	var limit = int.parse(args[0]), half = limit ~/ 2,
		sieve = List.filled(half, true), total = 1;
	for (var i = 3, isqrt = sqrt(limit); i < isqrt; i += 2)
		if (sieve[i ~/ 2])
			for (var j = i * i ~/ 2; j < half; j += i) sieve[j] = false;
	for (var i = 1; i < half; i++)
		if (sieve[i]) {
			stdout.write(", ${2 * i + 1}");
			total++;
		}
	print("\nTotal: ${total}");
}