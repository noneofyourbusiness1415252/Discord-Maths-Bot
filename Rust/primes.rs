fn main() {
	print!("2");
	let (limit, mut total) = (std::env::args().collect::<Vec<String>>()[1].parse::<usize>().unwrap(), 1);
	let half = limit / 2;
	let mut sieve = vec![true; half];
	for i in (3..=(limit as f32).sqrt() as usize).step_by(2) {
		if sieve[i / 2] {
			for j in (i * i / 2..half).step_by(i) {
				sieve[j] = false;
			}
		}
	}
	for i in 1..half {
		if sieve[i] {
			print!(", {}", 2 * i + 1);
			total += 1;
		}
	}
	println!("\nTotal: {}", total);
}