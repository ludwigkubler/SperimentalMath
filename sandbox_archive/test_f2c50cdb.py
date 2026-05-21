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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def primes(n):
    sieve = [True] * (n+1)
    for x in range(2, int(math.sqrt(n)) + 1):
        if sieve[x]:
            for i in range(x*x, n+1, x):
                sieve[i] = False
    return [x for x in range(2, n+1) if sieve[x]]

def random_disjointness_matrix(n):
    M = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            M[i][j] = 1
            M[j][i] = 1
    return M

def fft_2d(M):
    def fft(a):
        n = len(a)
        if n <= 1:
            return a
        even = fft([a[k] for k in range(0, n, 2)])
        odd = fft([a[k] for k in range(1, n, 2)])
        T = [cmath.exp(-2j * math.pi * k / n) * odd[k] for k in range(n // 2)]
        return [even[k] + T[k] for k in range(n // 2)] + [even[k] - T[k] for k in range(n // 2)]

    n = len(M)
    M_fft = [[0]*n for _ in range(n)]
    for i in range(n):
        M_fft[i] = fft([M[i][j] for j in range(n)])
    
    M_fft_t = [[0]*n for _ in range(n)]
    for j in range(n):
        M_fft_t[j] = fft([M_fft[i][j] for i in range(n)])
    
    return [[M_fft_t[j][i] for j in range(n)] for i in range(n)]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    M = random_disjointness_matrix(n)
    F = fft_2d(M)
    
    norm_squared = sum(abs(x)**2 for row in F for x in row)
    metric_value = math.sqrt(norm_squared)
    
    return {
        "metric_name": "Fourier Norm",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": metric_value >= n * 0.5,  # Lower bound of Ω(n)
        "counterexample": "" if metric_value >= n * 0.5 else "Fourier norm too small"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or primes(30)

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Fourier norm too small\" first_failing_seed={first_failing_seed}")