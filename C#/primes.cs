using System;
class primes {
	static void Main(string[] args) {
		Console.Write(2);
		uint limit = uint.Parse(args[0]), half = limit / 2,
			 isqrt = (uint)Math.Sqrt(limit), total = 1;
		bool[] sieve = new bool[half];
		for (uint i = 3; i <= isqrt; i += 2)
			if (!sieve[i / 2])
				for (uint j = i * i / 2; j < half; j += i) sieve[j] = true;
		for (uint i = 1; i < half; i++)
			if (!sieve[i]) {
				Console.Write(", " + (2 * i + 1));
				total++;
			}
		Console.WriteLine("\nTotal: " + total);
	}
}