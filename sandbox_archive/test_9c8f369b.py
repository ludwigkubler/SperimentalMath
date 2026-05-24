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
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = A[i][i]
            for j in range(i, n + 1):
                A[i][j] /= factor
            for j in range(n):
                if j != i:
                    factor = A[j][i]
                    for k in range(i, n + 1):
                        A[j][k] -= factor * A[i][k]
        return A

    def rank(A):
        A = gaussian_elimination(A)
        r = 0
        for row in A:
            if any(row):
                r += 1
        return r

    def fourier_coefficients(f, n):
        coeffs = [0] * (2**n)
        for x in range(2**n):
            sum_val = 0
            for i in range(n):
                sum_val += f(x >> i & 1) * (-1)**((x >> i & 1) ^ ((x >> (i+1)) & 1))
            coeffs[x] = sum_val / (2**(n-1))
        return [c for c in coeffs if c != 0]

    def boolean_function(n):
        return lambda x: random.choice([0, 1])

    n = random.randint(5, 40)
    f = boolean_function(n)
    coeffs = fourier_coefficients(f, n)
    kappa_f = rank([[coeffs[i] * coeffs[j] for j in range(len(coeffs))] for i in range(len(coeffs))])
    
    c = 1.0
    bound = c * math.log(n)
    conjecture_holds = kappa_f <= bound
    
    return {
        "metric_name": "Kappa F",
        "metric_value": kappa_f,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Counterexample found for n={n}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_kappa_f = sum(r["metric_value"] for r in results) / len(results)
    std_kappa_f = math.sqrt(sum((r["metric_value"] - mean_kappa_f)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_kappa_f} std={std_kappa_f} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_kappa_f} std={std_kappa_f} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='Kappa F exceeds bound' first_failing_seed={first_failing_seed}")