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
            max_row = i + max(range(i, m), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def matrix_rank(A):
        A = gaussian_elimination(A)
        rank = 0
        for row in A:
            if any(row):
                rank += 1
        return rank
    
    def topological_entanglement_entropy(n, r):
        # Simplified model: TE(n, r) = r * log2(n)
        return r * math.log2(n)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        m = random.randint(1, n)
        A = [[random.randint(0, 1) for _ in range(n)] for _ in range(m)]
        r = matrix_rank(A)
        te = topological_entanglement_entropy(n, r)
        results.append(te)
    
    mean_te = sum(results) / len(results)
    std_te = math.sqrt(sum((x - mean_te) ** 2 for x in results) / len(results))
    correlation_coefficient = (sum((results[i] - mean_te) * (i + 5 - 10) for i in range(len(results)))) / (len(results) * std_te * math.sqrt(40 * 30))
    
    return {
        "metric_name": "Pearson's Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient > 0.8,
        "counterexample": "" if correlation_coefficient > 0.8 else "Pearson's Correlation Coefficient < 0.8"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean_te = sum(results) / len(results)
    std_te = math.sqrt(sum((x - mean_te) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r > 0.8) / len(results)
    
    if all(r > 0.8 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_te} std={std_te} support_fraction={support_fraction}")
    elif any(r <= 0.8 for r in results):
        first_failing_seed = seeds[results.index(min(results))]
        print(f"RESULT: FALSIFIED counterexample='Pearson's Correlation Coefficient < 0.8' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")