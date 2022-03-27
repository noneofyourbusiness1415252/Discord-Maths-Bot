interface primes {
	static void main(String[] args) {
		System.out.print(2);
		int limit = Integer.parseUnsignedInt(args[0]),
			half = Integer.divideUnsigned(limit, 2),
			isqrt = (int) Math.sqrt(limit), total = 1;
		boolean[] sieve = new boolean[half];
		for (int i = 3; i <= isqrt; i += 2)
			if (!sieve[i / 2])
				for (int j = i * i / 2; j < half; j += i) sieve[j] = true;
		for (int i = 1; i < half; i++)
			if (!sieve[i]) {
				System.out.print(", " + Integer.toUnsignedString(2 * i + 1));
				total++;
			}
		System.out.printf("\nTotal: %d\n", total);
	}
}