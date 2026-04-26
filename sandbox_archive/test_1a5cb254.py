import random
import math
import sys

# Set a fixed seed for reproducibility
_rng = random.Random(42)

# --- Number Theory Helper Functions for Modular Forms Dimension ---

def get_divisors(n):
    """Returns a list of all divisors of n."""
    divs = set()
    for i in range(1, int(math.sqrt(n)) + 1):
        if n % i == 0:
            divs.add(i)
            divs.add(n // i)
    return sorted(list(divs))

def prime_factorize(n):
    """Returns a dictionary of prime factors and their powers."""
    factors = {}
    d = 2
    temp = n
    while d * d <= temp:
        while temp % d == 0:
            factors[d] = factors.get(d, 0) + 1
            temp //= d
        d += 1
    if temp > 1:
        factors[temp] = factors.get(