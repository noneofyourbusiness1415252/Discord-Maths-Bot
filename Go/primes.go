package main
import ("math"; "os"; "strconv")
func main() {
	print(2)
	limit, _ := strconv.ParseUint(os.Args[1], 10, 32)
	half := uint32(limit / 2)
	sieve, total := make([]bool, half), 1
	isqrt := uint32(math.Sqrt(float64(limit)))
	for i := uint32(3); i <= isqrt; i += 2 {
		if !sieve[i / 2] {
			for j := i * i / 2; j < half; j += i {
				sieve[j] = true
			}
		}
	}
	for i := uint32(1); i < half; i++ {
		if !sieve[i] {
			print(", ", 2 * i + 1)
			total++
		}
	}
	println("\nTotal:", total)
}