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
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def generate_primes(min_val, max_val):
    primes = []
    for num in range(min_val, max_val + 1):
        if is_prime(num):
            primes.append(num)
    return primes

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    size = random.randint(10, 100)
    
    # Generate a read-twice branching program for IP_2
    bp = [[random.randint(0, 1) for _ in range(n)] for _ in range(size)]
    
    # Compute the transition matrix entries
    T = [[0] * n for _ in range(n)]
    for i in range(size):
        for j in range(n):
            if bp[i][j] == 1:
                T[j][i % n] += 1
    
    # Calculate free cumulants via R-transform inversion formula (simplified)
    def r_transform(z, p):
        return z - p / (z + 1)
    
    def inv_r_transform(z, p):
        return (z * (z + 1) + p) / (z * (z + 1) - p)
    
    def free_cumulant(p):
        if p == 0:
            return 0
        z = complex(0.5, 0.5)
        for _ in range(10):  # Iterative refinement
            z = inv_r_transform(z, p)
        return z.real
    
    cumulants = [free_cumulant(T[i][i]) for i in range(n)]
    
    k = math.ceil(math.log2(n))
    sum_of_first_k_cumulants = sum(cumulants[:k])
    
    # Check the conjecture
    if n <= 10:
        expected_bound = 1
    else:
        expected_bound = math.log(size)
    
    conjecture_holds = sum_of_first_k_cumulants >= expected_bound
    
    return {
        "metric_name": "sum_of_first_k_cumulants",
        "metric_value": sum_of_first_k_cumulants,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Sum of first {k} cumulants: {sum_of_first_k_cumulants}, Expected bound: {expected_bound}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        primes = generate_primes(2, 100)
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results) and support_fraction >= 0.8:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")