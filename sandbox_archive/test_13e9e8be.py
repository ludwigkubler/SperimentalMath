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
            max_row = i + max(range(i, m), key=lambda j: abs(A[j][i]))
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            if pivot == 0:
                continue
            for j in range(n):
                A[i][j] /= pivot
            for k in range(m):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def char_poly(A):
        n = len(A)
        x = [1] + [0] * (n - 1)
        for i in range(1, n + 1):
            x_new = [0] * (n + 1)
            x_new[0] = -A[i-1][i-1]
            for j in range(n):
                x_new[j+1] = sum(A[i-1][k] * x[j-k] for k in range(j+1))
            x = x_new
        return x

    def min_root_separation(poly):
        n = len(poly)
        roots = []
        for i in range(1, n):
            if poly[i] != 0:
                root = -poly[0] / poly[i]
                roots.append(root)
        roots.sort()
        sep = float('inf')
        for i in range(1, len(roots)):
            sep = min(sep, abs(roots[i] - roots[i-1]))
        return sep

    def generate_cnf(size):
        cnf = []
        for _ in range(size):
            clause = [random.randint(-size, size) for _ in range(random.randint(2, 4))]
            cnf.append(clause)
        return cnf

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        size = random.randint(n, n * 2)
        cnf = generate_cnf(size)
        
        A = [[0] * (size + 1) for _ in range(size)]
        for clause in cnf:
            for literal in clause:
                if literal > 0:
                    row = literal - 1
                else:
                    row = -literal - 2
                A[row][size] += 1
                A[row][abs(literal) - 1] -= 1
        
        char_poly_coeffs = char_poly(A)
        min_sep = min_root_separation(char_poly_coeffs)
        
        results.append({
            "n": n,
            "size": size,
            "min_sep": min_sep
        })
    
    metric_value = sum(result["min_sep"] for result in results) / len(results)
    conjecture_holds = all(result["min_sep"] <= math.log(result["size"]) for result in results)
    counterexample = "" if conjecture_holds else f"n={results[0]['n']}, size={results[0]['size']}, min_sep={results[0]['min_sep']}"
    
    return {
        "metric_name": "minimal_root_separation",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['n']}, size={results[0]['size']}, min_sep={results[0]['min_sep']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")