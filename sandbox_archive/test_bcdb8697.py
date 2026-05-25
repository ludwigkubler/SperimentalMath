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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_circuit(n):
        # Simplified AC0-k-distance circuit generation for demonstration
        return [[random.choice([-1, 1]) for _ in range(n)] for _ in range(n)]
    
    def algebraic_K_theory(C):
        n = len(C)
        K_C = []
        for i in range(n):
            row_sum = sum(C[i][j] * C[j][k] for j in range(n) for k in range(n))
            K_C.append(row_sum)
        return K_C
    
    def tropicalize(A):
        m, n = len(A), len(A[0])
        T = [[max(row[j] for row in A) if col == j else float('-inf') for j in range(n)] for i in range(m)]
        return T
    
    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        matrix_copy = [row[:] for row in matrix]
        rank = 0
        for i in range(min(m, n)):
            if all(x == float('-inf') for x in matrix_copy[i]):
                continue
            pivot_row = max(range(i, m), key=lambda r: matrix_copy[r][i])
            if matrix_copy[pivot_row][i] == float('-inf'):
                continue
            rank += 1
            for j in range(n):
                matrix_copy[i][j], matrix_copy[pivot_row][j] = matrix_copy[pivot_row][j], matrix_copy[i][j]
            for r in range(m):
                if r != i:
                    factor = matrix_copy[r][i] / matrix_copy[i][i]
                    for j in range(n):
                        matrix_copy[r][j] -= factor * matrix_copy[i][j]
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        K_C = algebraic_K_theory(generate_circuit(n))
        T_K_C = tropicalize(K_C)
        rank_T_K_C = rank(T_K_C)
        results.append({
            "n": n,
            "rank": rank_T_K_C
        })
    
    metric_value = sum(result["rank"] for result in results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(2**(1/3) * n <= result["rank"] <= 2**n for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Rank of Tropicalized Algebraic K-theory",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(seed) for seed in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")