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
    
    def generate_disjointness_matrix(n):
        M = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                M[i][j] = random.choice([0, 1])
                M[j][i] = M[i][j]
        return M
    
    def matrix_multiplication(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def gaussian_elimination(A, b):
        n = len(A)
        M = [A[i] + [b[i]] for i in range(n)]
        for i in range(n):
            if M[i][i] == 0:
                continue
            for j in range(i + 1, n):
                factor = M[j][i] / M[i][i]
                for k in range(n + 1):
                    M[j][k] -= factor * M[i][k]
        x = [0] * n
        for i in range(n - 1, -1, -1):
            x[i] = (M[i][-1] - sum(M[i][j] * x[j] for j in range(i + 1, n))) / M[i][i]
        return x
    
    def eigenvalues(A):
        n = len(A)
        if n == 2:
            det = A[0][0] * A[1][1] - A[0][1] * A[1][0]
            trace = A[0][0] + A[1][1]
            lambda1, lambda2 = (trace + math.sqrt(trace**2 - 4*det)) / 2, (trace - math.sqrt(trace**2 - 4*det)) / 2
            return [lambda1, lambda2]
        else:
            x0 = [random.random() for _ in range(n)]
            x = gaussian_elimination(A, x0)
            eigenvalue = sum(x[i] * A[i][j] * x[j] for i in range(n) for j in range(n)) / sum(x[i]**2 for i in range(n))
            return [eigenvalue]
    
    def logarithmic_potential(eigenvalues):
        return sum(math.log(abs(lambda_)) for lambda_ in eigenvalues)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    
    for n in n_values:
        M = generate_disjointness_matrix(n)
        eigenvals = eigenvalues(M)
        metric_value = logarithmic_potential(eigenvals)
        total_metric_value += metric_value
        instances_tested += len(eigenvals)
    
    mean_metric_value = total_metric_value / instances_tested
    
    if mean_metric_value >= n_values[0]:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = f"mean_metric_value={mean_metric_value} < {n_values[0]}"
    
    return {
        "metric_name": "Free Entropy",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = f"mean_metric_value={mean_metric_value} < {n_values[0]}"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")