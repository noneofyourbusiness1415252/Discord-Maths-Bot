process.stdout.write('2')
half = ~~(process.argv[2] / 2)
sieve = new Uint8Array(half)
isqrt = ~~(Math.sqrt(process.argv[2]))
for (i = 3; i <= isqrt; i += 2)
if (!sieve[~~(i / 2)])
for (j = ~~(i ** 2 / 2); j < half; j += i) sieve[j] = true
total = 1
for (i = 1; i < half; i++)
if (!sieve[i]) {
	process.stdout.write(', ' + (2 * i + 1))
	total++
}
console.log('\nTotal:', total)