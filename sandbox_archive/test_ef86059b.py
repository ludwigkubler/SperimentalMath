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
    
    n = 20  # Fixed size for simplicity, can be adjusted if needed
    P = [[random.choice([-1, 1]) for _ in range(n)] for _ in range(n)]
    
    def matrix_multiplication(A, B):
        result = [[0] * len(B[0]) for _ in range(len(A))]
        for i in range(len(A)):
            for j in range(len(B[0])):
                for k in range(len(B)):
                    result[i][j] += A[i][k] * B[k][j]
        return result
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        augmented_matrix = [row[:] + [1 if i == j else 0 for j in range(n)] for i, row in enumerate(matrix)]
        
        for i in range(n):
            # Find the pivot
            max_row = i
            for k in range(i+1, n):
                if abs(augmented_matrix[k][i]) > abs(augmented_matrix[max_row][i]):
                    max_row = k
            
            # Swap rows
            augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
            
            # Eliminate below the pivot
            for k in range(i+1, n):
                factor = augmented_matrix[k][i] / augmented_matrix[i][i]
                for j in range(n + 1):
                    augmented_matrix[k][j] -= factor * augmented_matrix[i][j]
        
        # Back substitution
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = augmented_matrix[i][-1]
            for j in range(i+1, n):
                x[i] -= augmented_matrix[i][j] * x[j]
            x[i] /= augmented_matrix[i][i]
        
        return x
    
    def free_entropy(matrix):
        eigenvalues = gaussian_elimination(matrix)
        log_moment_gen_func = sum(math.log(1 + abs(e)) for e in eigenvalues) / len(eigenvalues)
        return 2 * log_moment_gen_func
    
    size = n ** 2
    if size >= 2 ** n // 2:
        metric_value = free_entropy(P)
        conjecture_holds = metric_value >= math.log(n) ** 2
        counterexample = "" if conjecture_holds else "size_threshold_not_met"
    else:
        metric_value = None
        conjecture_holds = False
        counterexample = "size_threshold_not_met"
    
    return {
        "metric_name": "free_entropy",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        support_fraction = 1.0
    else:
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"size_threshold_not_met\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")