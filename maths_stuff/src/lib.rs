extern crate cpython;
use cpython::*;
py_module_initializer! {maths_stuff, |py, m| {
m.add(py, "primesupto",
py_fn!(py, primesupto(n: usize) -> PyResult<Vec<usize>> {
	let mut sieve = vec![true; n / 2];
	(3..=(n as f32).sqrt() as usize).step_by(2).for_each(|i|
		if sieve[i / 2] {
			(i * i / 2..n / 2).step_by(i).for_each(|j| sieve[j] = false)
		});
	Ok((2..3).chain((1..n / 2).filter(|x| sieve[*x]).map(|x| 2 * x + 1)).collect())
}))?;
m.add(py, "nthpowers",
py_fn!(py, nthpowers(start: u64, end: u64) -> PyResult<String> {
	let mut fmt = String::new();
	if start == 1 {
		fmt += "1ⁿ = 1\nn⁰ = 1\n"
	}
	for i in start..=end {
		for j in 2..=(i as f32).sqrt() as u64 {
			let base = ((i as f32).powf(1. / (j as f32))).round() as u64;
			if base.pow(j as u32) == i {
				fmt += &format!("{}{} = {}\n", base, j.to_string().replace("0", "⁰").replace("1", "¹").replace("2", "²").replace("3", "³").replace("4", "⁴").replace("5", "⁵").replace("6", "⁶").replace("7", "⁷").replace("8", "⁸").replace("9", "⁹"), i)
			}
		}
	}
	Ok(fmt)
}))
}}
