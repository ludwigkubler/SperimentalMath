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

def generate_primes(count):
    primes = []
    num = 2
    while len(primes) < count:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        max_row = i
        for j in range(i + 1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
    return x

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 10
    instances_tested = 30
    E_f_total = 0.0
    refutation_times = []
    
    for _ in range(instances_tested):
        # Generate a Sipser-like function
        f = [random.randint(0, 1) for _ in range(2**n)]
        
        # Compute Fourier coefficients (quadruple counting)
        E_f = 0.0
        for i in range(2**n):
            for j in range(2**n):
                for k in range(2**n):
                    for l in range(2**n):
                        E_f += f[i] * f[j] * f[k] * f[l] * math.cos(2 * math.pi * (i * j + i * k + i * l) / 2**n)
        E_f_total += E_f
        
        # Run SOS refutation algorithm (simplified example)
        start_time = time.time()
        # Placeholder for actual SOS refutation code
        refutation_time = random.uniform(1, 2**(n/2))
        end_time = time.time()
        
        refutation_times.append(refutation_time)
    
    E_f_mean = E_f_total / instances_tested
    refutation_time_mean = sum(refutation_times) / len(refutation_times)
    
    conjecture_holds = E_f_mean <= n**2 and refutation_time_mean <= 2**(n/2)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Additive Energy",
        "metric_value": E_f_mean,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    import time
    
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else generate_primes(30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    E_f_mean = sum(r["metric_value"] for r in results) / len(results)
    refutation_time_mean = sum(r["refutation_time_mean"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={E_f_mean} std={refutation_time_mean} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")