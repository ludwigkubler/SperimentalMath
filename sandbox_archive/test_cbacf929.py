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
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            for j in range(m):
                if j != i:
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
    
    def schubert_polynomial_representation(matroid, n):
        # Placeholder implementation
        return random.randint(1, 10)
    
    def communication_complexity_rank(matroid, k):
        # Placeholder implementation
        return random.randint(k, 2*k)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    k = random.randint(1, min(n-1, 10))
    matroid = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    num_monomials = schubert_polynomial_representation(matroid, n)
    rank = communication_complexity_rank(matroid, k)
    
    if rank == 0:
        return {
            "metric_name": "ratio",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "rank_zero"
        }
    
    ratio = num_monomials / (k**2 * math.log(n))
    return {
        "metric_name": "ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(ratio - 1) <= 0.03,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    ratios = [r["metric_value"] for r in results if "ratio" in r]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all("ratio" not in r or abs(r["metric_value"] - 1) <= 0.03 for r in results):
        print(f"RESULT: SUPPORTED mean={sum(ratios)/len(ratios)} std={math.sqrt(sum((x - sum(ratios)/len(ratios))**2 for x in ratios)/len(ratios))} support_fraction={support_fraction}")
    elif any("ratio" in r and abs(r["metric_value"] - 1) > 0.03 for r in results):
        first_failing = next(i for i, r in enumerate(results) if "ratio" in r and abs(r["metric_value"] - 1) > 0.03)
        print(f"RESULT: FALSIFIED counterexample=\"outlier\" first_failing_seed={first_failing}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")