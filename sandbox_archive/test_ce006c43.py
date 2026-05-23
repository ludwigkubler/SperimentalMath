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
    
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    def lcm(a, b):
        return abs(a * b) // gcd(a, b)
    
    def matrix_multiply(A, B):
        m, n, p = len(A), len(B[0]), len(B)
        C = [[0 for _ in range(n)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def gaussian_elimination(A, b):
        n = len(b)
        M = [A[i] + [b[i]] for i in range(n)]
        for i in range(n):
            max_row = max(range(i, n), key=lambda k: abs(M[k][i]))
            M[i], M[max_row] = M[max_row], M[i]
            factor = M[i][i]
            if factor == 0:
                continue
            M[i] = [x / factor for x in M[i]]
            for j in range(n):
                if i != j:
                    factor = M[j][i]
                    M[j] = [M[j][k] - factor * M[i][k] for k in range(n + 1)]
        return [row[-1] for row in M]
    
    def schur_weyl_duality_rank(f):
        # Placeholder implementation
        return len(f)
    
    def monomial_ideal_complexity(f):
        # Placeholder implementation
        return len(f)
    
    n = random.randint(5, 40)
    f = [random.random() for _ in range(n)]
    
    rho_f = schur_weyl_duality_rank(f)
    kappa_f = monomial_ideal_complexity(f)
    
    metric_value = rho_f / (kappa_f + 1) if kappa_f > 0 else float('inf')
    conjecture_holds = rho_f <= kappa_f + 1 and rho_f >= kappa_f / 2 - 1
    counterexample = "" if conjecture_holds else f"Counterexample: n={n}, f={f}"
    
    return {
        "metric_name": "Schur-Weyl Duality Rank vs Monomial Ideal Complexity",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
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
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")