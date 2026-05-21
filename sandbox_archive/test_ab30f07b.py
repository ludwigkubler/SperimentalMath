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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        pivot = A[i][i]
        for j in range(i+1, n):
            factor = A[j][i] / pivot
            for k in range(n):
                A[j][k] -= factor * A[i][k]

    # Back substitution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = A[i][-1]
        for j in range(i+1, n):
            x[i] -= A[i][j] * x[j]
        x[i] /= A[i][i]
    
    return x

def spectral_gap(A):
    n = len(A)
    eigenvalues = []
    for _ in range(20):  # Run a few iterations of power method
        v = [random.random() for _ in range(n)]
        v /= sum(v) ** 0.5
        for _ in range(10):
            Av = [sum(A[i][j] * v[j] for j in range(n)) for i in range(n)]
            v = Av
            v /= sum(v) ** 0.5
        lambda_i = sum(Av[i] * v[i] for i in range(n))
        eigenvalues.append(lambda_i)
    
    return max(eigenvalues) - min(eigenvalues)

def construct_symplectic_matrix(dnf):
    n = len(dnf)
    A = [[0] * (2*n) for _ in range(2*n)]
    for i, clause in enumerate(dnf):
        for literal in clause:
            if literal > 0:
                A[i][literal-1] = 1
            else:
                A[2*n+i][-literal-1] = 1
    return A

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    dnf = [[random.choice([-i, i]) for _ in range(n)] for _ in range(random.randint(2, n))]
    
    A = construct_symplectic_matrix(dnf)
    gap = spectral_gap(A)
    
    metric_value = gap
    instances_tested = 1
    conjecture_holds = gap >= n**0.5 * math.log(n) and gap <= math.log(n)**2
    counterexample = "" if conjecture_holds else "spectral_gap_out_of_bounds"
    
    return {
        "metric_name": "Spectral Gap",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = (sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))**0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.2f} std={std_value:.2f} support_fraction={support_fraction:.2f}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"spectral_gap_out_of_bounds\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")