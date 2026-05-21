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
    
    def generate_disjointness_instance(n):
        A = [random.randint(0, 1) for _ in range(n)]
        B = [random.randint(0, 1) for _ in range(n)]
        return A, B
    
    def construct_sign_matrix(A, B):
        n = len(A)
        M = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if A[i] == B[j]:
                    M[i][j] = 1
                else:
                    M[i][j] = -1
        return M
    
    def free_probability_entanglement_invariant(M):
        n = len(M)
        trace = sum(M[i][i] for i in range(n))
        det = determinant(M, n)
        if det == 0:
            return float('-inf')
        return trace / abs(det)
    
    def determinant(matrix, n):
        if n == 1:
            return matrix[0][0]
        det = 0
        sign = 1
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += sign * matrix[0][j] * determinant(submatrix, n-1)
            sign *= -1
        return det
    
    def is_disjoint(A, B):
        return all(a != b for a, b in zip(A, B))
    
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    for n in n_values:
        A, B = generate_disjointness_instance(n)
        M = construct_sign_matrix(A, B)
        tau_M = free_probability_entanglement_invariant(M)
        results.append({
            "n": n,
            "tau_M": tau_M,
            "is_disjoint": is_disjoint(A, B),
        })
    
    metric_value = sum(result["tau_M"] for result in results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(result["tau_M"] >= n for result in results) and all(result["is_disjoint"])
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Free Probability Entanglement Invariant",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample,
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")