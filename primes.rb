# frozen_string_literal: true

print 2
limit = ARGV[0].to_i
half = limit / 2
sieve = "\x1" * half
total = 1
(3..Integer.sqrt(limit)).step(2).each do |i|
	next unless sieve[i / 2] == "\x1"

	(i**2 / 2...half).step(i).each do |j|
		sieve[j] = "\x0"
	end
end
(1...half).each do |i|
	if sieve[i] == "\x1"
		print ', ', 2 * i + 1
		total += 1
	end
end
puts "\nTotal: #{total}"
