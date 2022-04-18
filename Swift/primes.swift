print(terminator: "2")
let limit = UInt32(CommandLine.arguments[1])!, half = Int(limit / 2)
var sieve = [Bool](repeating: true, count: half), total = 1
for i in stride(from: 3, through: Int(Float(limit).squareRoot()), by: 2) {
	if sieve[i / 2] {
		for j in stride(from: i * i / 2, to: half, by: i) {
			sieve[j] = false
		}
	}
}
for i in stride(from: 1, to: half, by: 1) {
	if sieve[i] {
		print(",", 2 * i + 1, terminator: "")
		total += 1
	}
}
print("\nTotal:", total)