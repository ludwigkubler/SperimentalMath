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
            if pivot == 0:
                continue
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i and A[j][i] != 0:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def matrix_rank(A):
        rank = 0
        A = gaussian_elimination(A)
        for row in A:
            if any(row):
                rank += 1
        return rank
    
    def geometric_entropy(C):
        q = len(C[0])
        n = int(math.log2(q))
        H = 0
        for i in range(n):
            for j in range(n):
                if C[i][j] != 0:
                    H -= C[i][j] * math.log2(C[i][j])
        return H
    
    def generate_non_singular_curve(q, n):
        C = [[random.randint(0, q-1) for _ in range(n)] for _ in range(n)]
        while not is_non_singular(C):
            C = [[random.randint(0, q-1) for _ in range(n)] for _ in range(n)]
        return C
    
    def is_non_singular(C):
        det = 0
        n = len(C)
        if n == 2:
            det = C[0][0] * C[1][1] - C[0][1] * C[1][0]
        elif n == 3:
            det = (C[0][0] * (C[1][1] * C[2][2] - C[1][2] * C[2][1]) -
                   C[0][1] * (C[1][0] * C[2][2] - C[1][2] * C[2][0]) +
                   C[0][2] * (C[1][0] * C[2][1] - C[1][1] * C[2][0]))
        else:
            return False
        return det != 0
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        q = 2**n
        C = generate_non_singular_curve(q, n)
        H_C = geometric_entropy(C)
        r_C = matrix_rank(C)
        results.append({
            "n": n,
            "H_C": H_C,
            "r_C": r_C
        })
    
    mean_H_C = sum(result["H_C"] for result in results) / len(results)
    mean_r_C = sum(result["r_C"] for result in results) / len(results)
    std_H_C = math.sqrt(sum((result["H_C"] - mean_H_C)**2 for result in results) / len(results))
    std_r_C = math.sqrt(sum((result["r_C"] - mean_r_C)**2 for result in results) / len(results))
    
    conjecture_holds = all(abs(result["H_C"] - result["r_C"]) <= 3 for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "geometric_entropy",
        "metric_value": mean_H_C,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        seeds = [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_H_C = sum(result["metric_value"] for result in results) / len(results)
    std_H_C = math.sqrt(sum((result["metric_value"] - mean_H_C)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_H_C} std={std_H_C} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")