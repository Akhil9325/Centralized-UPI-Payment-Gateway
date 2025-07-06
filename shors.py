import numpy as np
from math import gcd
from fractions import Fraction
from random import randint

def euclidGCD(n, m):
    if m == 0:
        return n
    return euclidGCD(m, n % m)

def classical_period_finding(a, N):
    r = 1
    while pow(a, r, N) != 1:
        r += 1
        if r > N:
            return None
    return r

def shors_classical(N):
    if N % 2 == 0:
        return 2
    attempt = 0
    while True:
        attempt += 1
        a = randint(2, N - 1)
        print(f"Attempt {attempt}: Trying a = {a}")
        if gcd(a, N) != 1:
            print(f"GCD({a}, {N}) = {gcd(a, N)}. Found factor early!")
            return gcd(a, N)

        r = classical_period_finding(a, N)
        if r is None or r % 2 != 0:
            print(f"Invalid period r = {r}")
            continue

        if pow(a, r, N) != 1:
            continue

        plus = gcd(pow(a, r // 2) + 1, N)
        minus = gcd(pow(a, r // 2) - 1, N)

        for factor in [plus, minus]:
            if factor != 1 and factor != N and N % factor == 0:
                print(f"Success! Found non-trivial factor: {factor}")
                return factor

N = 65
factor = shors_classical(N)
print(f"One factor of {N} is {factor}")