extern crate cpython;
use cpython::*;
py_module_initializer! {primes, |py, m| {m.add(py, "primesupto", py_fn!(py, primesupto(n: usize)))}}
fn primesupto(_: Python, n: usize) -> PyResult<Vec<usize>> {
	let mut sieve = vec![true; n / 2];
	(3..=(n as f32).sqrt() as usize).step_by(2).for_each(|i| {
		if sieve[i / 2] {
			(i * i / 2..n / 2).step_by(i).for_each(|j| sieve[j] = false)
		}
	});
	Ok((2..3)
		.chain((1..n / 2).filter(|x| sieve[*x]).map(|x| 2 * x + 1))
		.collect())
}
