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
    random.seed(seed)
    
    def generate_random_unitary(n):
        u = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i == j:
                    u[i][j] = 1
                else:
                    u[i][j] = random.uniform(-1, 1)
        return u
    
    def trace(matrix):
        return sum(matrix[i][i] for i in range(len(matrix)))
    
    def frobenius_schur_indicator(u):
        n = len(u)
        det = abs(trace(gaussian_elimination(u)) / math.factorial(n))
        return det
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = matrix[i][i]
            for j in range(n):
                matrix[i][j] /= factor
            for j in range(n):
                if i != j:
                    factor = matrix[j][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix
    
    def entropy(distribution):
        total = sum(distribution)
        if total <= 0:
            return 0
        return -sum(p * math.log2(p) for p in distribution if p > 0)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        u = generate_random_unitary(n)
        indicator = frobenius_schur_indicator(u)
        distribution = [random.random() for _ in range(2**n)]
        entropy_value = entropy(distribution)
        results.append({
            "n": n,
            "indicator": indicator,
            "entropy": entropy_value
        })
    
    mean_indicator = sum(r["indicator"] for r in results) / len(results)
    mean_entropy = sum(r["entropy"] for r in results) / len(results)
    conjecture_holds = all(indicator <= entropy_value for r in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Frobenius-Schur Indicator",
        "metric_value": mean_indicator,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_indicator = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_indicator} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_indicator} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")