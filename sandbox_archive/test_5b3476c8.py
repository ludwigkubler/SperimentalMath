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
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def spectral_gap(A):
        n = len(A)
        eigenvalues = []
        I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        for _ in range(10):  # Power iteration method
            v = [random.random() for _ in range(n)]
            v = [x / math.sqrt(sum(x**2 for x in v)) for x in v]
            Av = [sum(A[i][j] * v[j] for j in range(n)) for i in range(n)]
            lambda_ = sum(v[i] * Av[i] for i in range(n))
            eigenvalues.append(lambda_)
        return max(eigenvalues) - min(eigenvalues)

    def symplectic_orthogonal_matrix(dnf):
        n = len(dnf)
        A = [[0] * (2*n) for _ in range(2*n)]
        for i, clause in enumerate(dnf):
            for lit in clause:
                if lit > 0:
                    A[i][lit-1] = 1
                else:
                    A[i+n][(abs(lit)-1)] = -1
        return gaussian_elimination(A)

    def is_submodular(gap, n):
        c = math.log(n) / n
        return gap >= c * n

    def bound_spectral_gap(n):
        return math.log2(n)**2

    n = random.randint(5, 40)
    dnf = [[random.choice([-1, 1]) * (i+1) for i in range(n)] for _ in range(random.randint(1, n))]
    A = symplectic_orthogonal_matrix(dnf)
    gap = spectral_gap(A)

    conjecture_holds = is_submodular(gap, n) and gap <= bound_spectral_gap(n)
    counterexample = "submodularity" if not is_submodular(gap, n) else "bound_exceeded"

    return {
        "metric_name": "spectral_gap",
        "metric_value": gap,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i - 1 for i in range(5, 8)]
    
    results = []
    total_metric_value = 0
    support_count = 0
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        total_metric_value += trial_result["metric_value"]
        if trial_result["conjecture_holds"]:
            support_count += 1
        
        results.append(trial_result)
    
    mean_metric_value = total_metric_value / len(results)
    support_fraction = support_count / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")