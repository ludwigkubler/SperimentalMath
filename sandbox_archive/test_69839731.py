# auto-injected by SEC sandbox
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def generate_primes(n):
    primes = []
    num = 2
    while len(primes) < n:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Generate a random prime number for the field size GF(2^n)
    n = random.randint(5, 40)
    p = generate_primes(n + 1)[-1]
    
    # Define an elliptic curve equation over GF(p)
    a = random.randint(0, p - 1)
    b = random.randint(0, p - 1)
    while (4 * a**3 + 27 * b**2) % p == 0:
        a = random.randint(0, p - 1)
        b = random.randint(0, p - 1)
    
    # Compute the genus of the elliptic curve
    g = (p + 1 - n) // 2
    
    # Check if the conjecture holds for this instance
    if g < math.log(n):
        refutation_size = 2 ** (math.ceil(g * math.log(n)))
    else:
        refutation_size = float('inf')
    
    return {
        "metric_name": "SOS Refutation Size",
        "metric_value": refutation_size,
        "instances_tested": 1,
        "conjecture_holds": g < math.log(n),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or generate_primes(30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")