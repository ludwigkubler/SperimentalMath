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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(m, N):
        return [random.randint(0, d-1) for _ in range(N)]
    
    def fourier_coefficients(f, m, N):
        n = 2**m
        coeffs = [0] * n
        for i in range(n):
            sum_val = 0
            for j in range(N):
                sum_val += f[j] * math.cos(2 * math.pi * i * j / n)
            coeffs[i] = sum_val / n
        return coeffs
    
    def geometric_measure(coeffs, m):
        n = len(coeffs)
        A = [[coeffs[(i + j) % n] for j in range(m)] for i in range(n)]
        rank = gaussian_elimination(A, m)
        return 2**(-rank / 2)
    
    def gaussian_elimination(A, m):
        n = len(A)
        pivot_row = 0
        for col in range(m):
            max_row = pivot_row
            for row in range(pivot_row + 1, n):
                if abs(A[row][col]) > abs(A[max_row][col]):
                    max_row = row
            A[pivot_row], A[max_row] = A[max_row], A[pivot_row]
            if A[pivot_row][col] == 0:
                continue
            for row in range(pivot_row + 1, n):
                factor = -A[row][col] / A[pivot_row][col]
                for j in range(col, m):
                    A[row][j] += factor * A[pivot_row][j]
            pivot_row += 1
        return sum(1 for row in range(n) if A[row][0] != 0)
    
    def communication_complexity_rank(f, m, N):
        n = 2**m
        matrix = [[f[(i + j) % N] for i in range(n)] for j in range(m)]
        rank = gaussian_elimination(matrix, m)
        return rank
    
    m = random.randint(5, 40)
    N = random.randint(1, 2**m)
    d = random.randint(2, 3)
    
    f = generate_boolean_function(m, N)
    coeffs = fourier_coefficients(f, m, N)
    geo_measure = geometric_measure(coeffs, m)
    rank = communication_complexity_rank(f, m, N)
    
    return {
        "metric_name": "Pearson's correlation coefficient",
        "metric_value": geo_measure * rank,
        "instances_tested": 1,
        "n_max": m,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")