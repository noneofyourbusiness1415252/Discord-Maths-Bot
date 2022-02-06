from sys import argv
print(end="2")
limit = int(argv[1])
half = limit // 2
sieve, total = bytearray({True}) * half, 1
for i in range(3, int(limit ** 0.5) + 1, 2):
	if sieve[i // 2]:
		for j in range(i ** 2 // 2, half, i):
			sieve[j] = False
for i in range(1, half):
	if sieve[i]:
		print(",", 2 * i + 1, end="")
		total += 1
print("\nTotal:", total)