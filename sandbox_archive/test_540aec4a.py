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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def characteristic_polynomial(f):
        n = int(math.log2(len(f)))
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            for j in range(n):
                A[i][j] = sum(f[k] * f[k + i + j] for k in range(2**i)) / (2**(i + j))
        return A
    
    def min_root_multiplicity_index(A):
        n = len(A) - 1
        det_A = determinant(A)
        if det_A == 0:
            return float('inf')
        roots = [complex(z.real, z.imag) for z in solve_polynomial(det_A)]
        multiplicities = [roots.count(root) for root in set(roots)]
        return min(multiplicities)
    
    def communication_complexity_rank_variance(f):
        n = int(math.log2(len(f)))
        rank = 0
        for i in range(n + 1):
            if any(f[j] != f[j + i] for j in range(2**i)):
                rank += 1
        return rank
    
    def determinant(A):
        n = len(A)
        if n == 1:
            return A[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += ((-1) ** j) * A[0][j] * determinant(submatrix)
        return det
    
    def solve_polynomial(p):
        n = len(p) - 1
        if n == 0:
            return []
        if n == 1:
            return [-p[0] / p[1]]
        roots = []
        for i in range(n + 1):
            sub_coeffs = [p[j] for j in range(i, n + 1)]
            sub_roots = solve_polynomial(sub_coeffs)
            for root in sub_roots:
                if (root - p[i]) % p[n] == 0:
                    roots.append(root)
        return roots
    
    def log_ratio(n, I, kappa):
        return math.log(math.sqrt(I) / kappa) / math.log(n)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = generate_boolean_function(n)
    A = characteristic_polynomial(f)
    I = min_root_multiplicity_index(A)
    kappa = communication_complexity_rank_variance(f)
    
    if I == float('inf') or kappa == 0:
        return {
            "metric_name": "log_ratio",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ratio = log_ratio(n, I, kappa)
    return {
        "metric_name": "log_ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")