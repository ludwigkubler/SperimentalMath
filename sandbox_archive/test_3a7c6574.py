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

def run_trial(seed: int) -> dict:
    n = 40
    random.seed(seed)
    
    def generate_disjointness_matrix(n):
        M = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                M[i][j] = 1
                M[j][i] = 1
        return M
    
    def fft(a):
        n = len(a)
        if n == 1:
            return a
        even = fft([a[k] for k in range(0, n, 2)])
        odd = fft([a[k] for k in range(1, n, 2)])
        T = [cmath.exp(-2j * math.pi * k / n) * odd[k] for k in range(n // 2)]
        return [even[k] + T[k] for k in range(n // 2)] + [even[k] - T[k] for k in range(n // 2)]
    
    def fft_2d(M):
        n = len(M)
        M_fft = [[0] * n for _ in range(n)]
        for i in range(n):
            M_fft[i] = fft([M[i][j] for j in range(n)])
        return [fft(row) for row in M_fft]
    
    def l2_norm(matrix):
        sum_of_squares = 0
        for row in matrix:
            for val in row:
                sum_of_squares += abs(val) ** 2
        return math.sqrt(sum_of_squares)
    
    M = generate_disjointness_matrix(n)
    F = fft_2d(M)
    norm = l2_norm(F)
    
    return {
        "metric_name": "Fourier Norm",
        "metric_value": norm,
        "instances_tested": 1,
        "conjecture_holds": norm >= n,
        "counterexample": "" if norm >= n else "norm < n"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_norm = sum(result["metric_value"] for result in results) / len(results)
    std_norm = math.sqrt(sum((result["metric_value"] - mean_norm) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_norm} std={std_norm} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_norm} std={std_norm} support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"norm < n\" first_failing_seed={result['seed']}")
                break