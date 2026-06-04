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
    
    def lanczos_algorithm(A, v, k):
        n = len(A)
        alpha = [0] * (k + 1)
        beta = [0] * k
        Q = [[0] * k for _ in range(n)]
        Q[0][0] = v / math.sqrt(v @ A @ v)
        v = A @ Q[0][0]
        
        for i in range(1, k):
            alpha[i] = v @ A @ Q[i-1][i-1]
            v -= alpha[i] * Q[i-1][i-1]
            beta[i-1] = math.sqrt(v @ v)
            Q[i][i-1] = v / beta[i-1]
            v = A @ Q[i][i-1] - beta[i-1] * Q[i-1][i-1]
        
        alpha[k] = v @ A @ Q[k-1][k-1]
        return alpha, beta

    def spectral_gap(alpha, beta):
        n = len(alpha)
        eigenvalues = [alpha[0]]
        for i in range(1, n):
            eigenvalues.append(eigenvalues[-1] + alpha[i])
        
        min_gap = float('inf')
        for i in range(1, n):
            gap = abs(eigenvalues[i] - eigenvalues[i-1])
            if 0 < gap < min_gap:
                min_gap = gap
        
        return min_gap

    def generate_communication_instance(n, r):
        A = [[0] * n for _ in range(n)]
        for i in range(r):
            row = random.sample(range(n), 2)
            A[row[0]][row[1]] = A[row[1]][row[0]] = random.uniform(-1, 1)
        return A

    def matrix_rank(A):
        n = len(A)
        rank = 0
        for i in range(n):
            if any(A[j][i] != 0 for j in range(i, n)):
                rank += 1
        return rank

    def normalize(v):
        norm = math.sqrt(sum(x**2 for x in v))
        return [x / norm for x in v]

    def hermitian_form(A, v):
        return sum(A[i][j] * (v[i] * v[j] + v[i] * v[j]) for i in range(len(v)) for j in range(i+1, len(v)))

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            r = random.randint(1, min(n-1, 5))
            A = generate_communication_instance(n, r)
            v = normalize([random.uniform(-1, 1) for _ in range(n)])
            alpha, beta = lanczos_algorithm(A, v, r)
            gap = spectral_gap(alpha, beta)
            results.append({
                "n": n,
                "r": r,
                "gap": gap
            })
    
    if not results:
        return {
            "metric_name": "spectral_gap",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    instances_tested = len(results)
    n_max = max(result["n"] for result in results)
    conjecture_holds = all(result["gap"] >= result["r"] / math.log(result["n"]) for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "spectral_gap",
        "metric_value": sum(result["gap"] for result in results) / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{trial_result}...}}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")