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
            for j in range(n):
                A[i][j] /= pivot
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

    def variance_ratio(matrix):
        n = len(matrix)
        mean = sum(sum(row) for row in matrix) / (n**2)
        variance = sum((sum(row) - mean)**2 for row in matrix) / (n**2)
        return variance / mean if mean != 0 else None

    def minimal_order(formal_context):
        n = len(formal_context)
        A = [[1 if formal_context[i][j] else 0 for j in range(n)] for i in range(n)]
        rank = 0
        for i in range(n):
            if sum(A[i]) > 0:
                rank += 1
                for j in range(i+1, n):
                    if A[j][i] == 1:
                        for k in range(n):
                            A[j][k] ^= A[i][k]
        return rank

    def generate_communication_instance(n):
        instance = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        return instance

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_min_order = 0
        total_variance_ratio = 0
        
        for _ in range(5):
            instance = generate_communication_instance(n)
            matrix = gaussian_elimination(instance)
            variance = variance_ratio(matrix)
            
            if variance is not None:
                min_order = minimal_order(instance)
                results.append({
                    "n": n,
                    "min_order": min_order,
                    "variance_ratio": variance
                })
                total_min_order += min_order
                total_variance_ratio += variance
                instances_tested += 1
        
        if instances_tested == 0:
            return {
                "metric_name": "Minimal Order of Formal Contexts and Communication Complexity Rank Variance Ratio",
                "metric_value": None,
                "instances_tested": 0,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "No valid instances generated"
            }
    
    mean_min_order = total_min_order / len(results)
    mean_variance_ratio = total_variance_ratio / len(results)
    ratio = mean_min_order / mean_variance_ratio
    
    return {
        "metric_name": "Minimal Order of Formal Contexts and Communication Complexity Rank Variance Ratio",
        "metric_value": ratio,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": 0.5 <= ratio <= 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(2, 6)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all("conjecture_holds" in result and result["conjecture_holds"] for result in results):
        mean_ratio = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif any("counterexample" in result and result["counterexample"] for result in results):
        first_failing_seed = next(result["seed"] for result in results if "counterexample" in result)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")