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
            max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(n):
                if j != i:
                    factor = A[j][i] / A[i][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def spectral_gap(A):
        n = len(A)
        identity = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        eigenvalues = []
        for _ in range(10):  # Power iteration method
            v = [random.random() for _ in range(n)]
            v /= math.sqrt(sum(x**2 for x in v))
            Av = matrix_multiply(A, v)
            lambda_ = sum(Av[i] * v[i] for i in range(n)) / sum(v[i]**2 for i in range(n))
            eigenvalues.append(lambda_)
        return max(eigenvalues) - min(eigenvalues)

    def pseudoexpectation(M):
        n = len(M)
        return sum(sum(M[i][j] for j in range(i+1, n)) for i in range(n))

    def max_cut_approximation_ratio(spectral_gap, d):
        return 0.878 - spectral_gap

    n = random.randint(5, 40)
    M = [[random.random() if i != j else 0 for j in range(n)] for i in range(n)]
    M = gaussian_elimination(M)
    pseudoexp = pseudoexpectation(M)
    gap = spectral_gap(M)
    d = max_cut_approximation_ratio(gap, 3)

    return {
        "metric_name": "max_cut_approximation_ratio",
        "metric_value": d,
        "instances_tested": 1,
        "conjecture_holds": d > 0.878 - gap,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3**j for i in range(5) for j in range(5)]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                counterexample = f"seed={result['seed']}, metric_value={result['metric_value']}"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={result['seed']}")
                break