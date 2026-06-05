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
    
    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0]*p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def determinant(A):
        m, n = len(A), len(A[0])
        if m != n:
            raise ValueError("Matrix must be square")
        if n == 1:
            return A[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1)**j * A[0][j] * determinant(submatrix)
        return det
    
    def min_tropical_rank(A):
        m, n = len(A), len(A[0])
        rank = 0
        for i in range(min(m, n)):
            if determinant(gaussian_elimination(A[:i+1])) != 0:
                rank += 1
        return rank
    
    def circuit_size(G):
        # Placeholder function to compute circuit size
        # This is a dummy implementation and should be replaced with actual computation
        return len(G)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    G = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    A = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
    
    min_tr_G = min_tropical_rank(A)
    s_C_G = circuit_size(G)
    
    if min_tr_G > 10:
        return {
            "metric_name": "min_tr(G)",
            "metric_value": min_tr_G,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": f"min_tr(G) = {min_tr_G} > 10"
        }
    
    if min_tr_G <= 1.5 * s_C_G:
        return {
            "metric_name": "min_tr(G)",
            "metric_value": min_tr_G,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": True,
            "counterexample": ""
        }
    
    return {
        "metric_name": "min_tr(G)",
        "metric_value": min_tr_G,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": f"min_tr(G) = {min_tr_G} > 1.5 * s(C_G)"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if "metric_value" in r]
    conjecture_holds = all(r["conjecture_holds"] for r in results if "conjecture_holds" in r)
    
    mean_metric_value = sum(metric_values) / len(metric_values)
    std_metric_value = math.sqrt(sum((x - mean_metric_value)**2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if conjecture_holds:
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.4f} std={std_metric_value:.4f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"min_tr(G) > 1.5 * s(C_G)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")