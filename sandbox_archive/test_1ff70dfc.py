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
    n = 40
    p = 0.5
    c = 0.1
    
    random.seed(seed)
    
    def generate_random_graph(n, p):
        A = [[random.random() < p for _ in range(n)] for _ in range(n)]
        for i in range(n):
            A[i][i] = 0
        return A
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i + 1, m):
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
        return [abs(A[i][n-1]) for i in range(m)]
    
    def compute_sos_degree(d):
        # Placeholder function to simulate SOS degree
        return d
    
    def compute_smallest_singular_value(A):
        U, S, Vt = gaussian_elimination(A)
        return min(S)
    
    A = generate_random_graph(n, p)
    sigma_min = compute_smallest_singular_value(A)
    
    for d in range(1, 11):
        sos_degree = compute_sos_degree(d)
        if sigma_min < c * (d ** -1):
            return {
                "metric_name": "sigma_min",
                "metric_value": sigma_min,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"SOS degree {d} does not satisfy the conjecture"
            }
    
    return {
        "metric_name": "sigma_min",
        "metric_value": sigma_min,
        "instances_tested": 10,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        seeds = primes[:30]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"SOS degree does not satisfy the conjecture\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")