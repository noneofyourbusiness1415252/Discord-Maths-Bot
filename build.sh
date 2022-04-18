for i in $@; do
	cd ~/$REPL_SLUG/$i
	case $i in
	Java)
		javac primes.java
		java primes 1000
		;;
	C♯)
		csc primes.cs
		mkbundle -o primes --simple --no-machine-config --no-config primes.exe
		rm primes.exe
		;;
	C++)
		clang++ -Ofast -Wmost -o primes primes.cc
		;;
	C)
		clang -Ofast -Wmost -o primes primes.c
		;;
	Go)
		go build primes.go
		;;
	Kotlin)
		kotlinc primes.kt
		rm META-INF
		kotlin primes 1000
		;;
	Rust)
		rustc -C opt-level=3 primes.rs
		;;
	Dart)
		dart --snapshot-kind=app-jit --snapshot=primes primes.dart 1000
		;;
	Swift)
		swiftc -Ounchecked -Xlinker -lm primes.swift
		;;
	esac
	if [[ $i != @(Java|Kotlin|Dart) ]]; then
		./primes 1000
	fi
done
for ((x = 0; ; x++)); do
	printf "\x1b[38;5;$((x % 216 + 16))mFinished! Press enter to dismiss\a\r"
	if read -t 0.5; then
		exit
	fi
done