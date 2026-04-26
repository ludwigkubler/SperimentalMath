# auto-injected by SEC sandbox
import itertools
import collections
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
import sys
import json

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i + max(range(i, m), key=lambda k: abs(A[k][i]))
        A[i], A[max_row] = A[max_row], A[i]
        if A[i][i] == 0:
            raise ValueError("Matrix is singular")
        for j in range(n):
            A[i][j] /= A[i][i]
        for k in range(m):
            if k != i and A[k][i] != 0:
                factor = A[k][i]
                for j in range(n):
                    A[k][j] -= factor * A[i][j]
    return A

def matrix_multiply(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0 for _ in range(p)] for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def is_unsat(F, n):
    m = len(F)
    for x in range(1 << n):
        satisfied = all((x >> j) & 1 == (c >> j) & 1 for c in F)
        if not satisfied:
            return True
    return False

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [8, 10, 12]
    alpha = 4.5
    m_values = [int(alpha * n) for n in n_values]
    num_instances = 40
    
    results = []
    for n, m in zip(n_values, m_values):
        for _ in range(num_instances):
            F = []
            while len(F) < m:
                clause = random.randint(1, (1 << n) - 1)
                if not is_unsat([clause], n):
                    F.append(clause)
            
            g_F = sum((x >> j) & 1 == (c >> j) & 1 for c in F for x in range(1 << n)) - 7 * m / 8
            A = [[0] * (n + 1) for _ in range(n + 1)]
            for i in range(n):
                for j in range(n):
                    A[i][j] = sum((x >> k) & 1 == ((c >> k) & 1 ^ (c >> l) & 1) for c in F for x in range(1 << n))
                A[i][n] = g_F
            A[n][n] = m
            
            try:
                A = gaussian_elimination(A)
                norm_2 = sum(A[i][i] ** 2 for i in range(n)) ** 0.5
                norm_4 = sum(A[i][i] ** 4 for i in range(n)) ** 0.5
                HC_F = norm_4 / norm_2
                
                width = None
                for w in range(2, n + 1):
                    clauses_w = [c for c in F if bin(c).count('1') <= w]
                    if not is_unsat(clauses_w, n):
                        width = w
                        break
                
                results.append({
                    "n": n,
                    "m": m,
                    "g_F": g_F,
                    "norm_2": norm_2,
                    "norm_4": norm_4,
                    "HC_F": HC_F,
                    "width": width
                })
            except ValueError:
                return {
                    "metric_name": "resolution_width",
                    "metric_value": None,
                    "instances_tested": 1,
                    "conjecture_holds": False,
                    "counterexample": "mapping_undefined"
                }
    
    correlation = 0
    slope = float('inf')
    for result in results:
        if result["HC_F"] > 1.2 and result["width"] is not None:
            correlation += (result["width"] - n * math.log2(result["HC_F"]) / math.log2(n)) * (n * math.log2(result["HC_F"]) / math.log2(n) - sum(r["n"] * math.log2(r["HC_F"]) / math.log2(r["n"]) for r in results if r["HC_F"] > 1.2) / len([r for r in results if r["HC_F"] > 1.2]))
            slope = min(slope, result["width"] * math.log2(n) / (result["n"] * math.log2(result["HC_F"])))
    
    correlation /= sum((n * math.log2(HC_F) / math.log2(n) - sum(r["n"] * math.log2(r["HC_F"]) / math.log2(r["n"]) for r in results if r["HC_F"] > 1.2) / len([r for r in results if r["HC_F"] > 1.2])) ** 2 for result in results if result["HC_F"] > 1.2)
    
    return {
        "metric_name": "resolution_width",
        "metric_value": n * math.log2(HC_F) / math.log2(n),
        "instances_tested": len(results),
        "conjecture_holds": correlation >= 0.5 and slope >= 0.02,
        "counterexample": "" if correlation >= 0.5 and slope >= 0.02 else f"c*={slope} < 0.02"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    for seed in seeds:
        result = run_trial(seed)
        print(json.dumps({"TRIAL": {**result, "seed": seed}}))
    
    results = [run_trial(seed) for seed in seeds if result["conjecture_holds"]]
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = (sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = len(results) / len(seeds)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")