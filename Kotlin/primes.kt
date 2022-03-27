fun main(args: Array<String>) {
	print(2u)
	val limit = args[0].toUInt()
	val half = (limit / 2u).toInt()
	var (sieve, total) = BooleanArray(half) { true } to 1u
	for (i in 3..kotlin.math.sqrt(limit.toDouble()).toInt() step 2)
		if (sieve[i / 2])
			for (j in i * i / 2 until half step i)
				sieve[j] = false
	for (i in 1 until half)
		if (sieve[i]) {
			print(", ${2u * i.toUInt() + 1u}")
			total++
		}
	println("\nTotal: $total")
}