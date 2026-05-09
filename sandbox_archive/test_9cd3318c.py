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

def fast_walsh_hadamard_transform(arr):
    n = len(arr)
    if n == 1:
        return arr
    even = fast_walsh_hadamard_transform(arr[::2])
    odd = fast_walsh_hadamard_transform(arr[1::2])
    result = [0] * n
    for k in range(n // 2):
        result[k] = even[k] + odd[k]
        result[k + n // 2] = even[k] - odd[k]
    return result

def generate_cnf(n, m):
    cnf = []
    for _ in range(m):
        clause = [random.randint(1, n), random.randint(1, n), random.randint(1, n)]
        random.shuffle(clause)
        cnf.append(clause)
    return cnf

def compute_fourier_coefficients(cnf, n):
    num_vars = 2 ** n
    zero_vector = [0] * num_vars
    one_vector = [1] * num_vars
    for clause in cnf:
        var_indices = [1 << (abs(var) - 1) for var in clause]
        for i in range(num_vars):
            if all((i & idx) != 0 for idx in var_indices):
                zero_vector[i] += 1
            else:
                one_vector[i] += 1
    zero_fft = fast_walsh_hadamard_transform(zero_vector)
    one_fft = fast_walsh_hadamard_transform(one_vector)
    fourier_coefficients = [abs(z - o) / num_vars for z, o in zip(zero_fft, one_fft)]
    return min(fourier_coefficients)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(n * 2, min(n * 10, 100))
    cnf = generate_cnf(n, m)
    mu = compute_fourier_coefficients(cnf, n)
    c = 0.1
    conjecture_holds = mu >= c * math.sqrt(m)
    counterexample = "" if conjecture_holds else f"m={m}, mu={mu}"
    return {
        "metric_name": "Fourier Min-Coefficient",
        "metric_value": mu,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_mu = sum(r["metric_value"] for r in results) / len(results)
    std_mu = math.sqrt(sum((r["metric_value"] - mean_mu)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_mu} std={std_mu} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"m={result['counterexample']}\", first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")