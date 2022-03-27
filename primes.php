2<?php
$half = intdiv($argv[1], 2);
$sieve = str_repeat('1', $half);
for ($i = 3; $i <= (int)sqrt($argv[1]); $i += 2)
	if ($sieve[intdiv($i, 2)]) for ($j = intdiv($i ** 2, 2); $j < $half; $j += $i)
		$sieve[$j] = '0';
$total = 1;
for ($i = 1; $i < $half; $i++) if ($sieve[$i]) {
	echo ', ', 2 * $i + 1;
	$total++;
}
echo "\nTotal: {$total}\n";
?>