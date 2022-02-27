from ctypes import CDLL, c_uint, POINTER, byref
from sys import argv

primesupto = CDLL("./primes").primesupto
primesupto.restype = POINTER(c_uint)
total = c_uint()
primes = primesupto(
	int(
		argv[1]
		if len(argv) > 1
		else input("Enter a number to find the primes up to it: ")
	),
	byref(total),
)
print(primes[:total.value], "\nTotal:", total.value)