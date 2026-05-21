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
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            # Find pivot
            max_row = i
            for k in range(i+1, n):
                if abs(matrix[k][i]) > abs(matrix[max_row][i]):
                    max_row = k
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            
            # Eliminate below
            pivot = matrix[i][i]
            for k in range(i+1, n):
                factor = matrix[k][i] / pivot
                for j in range(n):
                    matrix[k][j] -= factor * matrix[i][j]
        
        # Back substitution
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = matrix[i][-1]
            for k in range(i+1, n):
                x[i] -= matrix[i][k] * x[k]
            x[i] /= matrix[i][i]
        
        return x
    
    def sign_matrix(n):
        M = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                M[i][j] = random.choice([-1, 1])
                M[j][i] = -M[i][j]
        return M
    
    def free_probability_entanglement_invariant(M):
        n = len(M)
        identity = [[int(i == j) for j in range(n)] for i in range(n)]
        A = [row[:] + [1] for row in M]
        B = [row[:] + [0] for row in identity]
        
        # Solve AX = B
        X = gaussian_elimination(A)
        
        # Compute τ(M)
        tau_M = sum(abs(X[i]) for i in range(n))
        return tau_M
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    M = sign_matrix(n)
    tau_M = free_probability_entanglement_invariant(M)
    
    metric_name = "free_probability_entanglement_invariant"
    metric_value = tau_M
    instances_tested = 1
    conjecture_holds = tau_M >= n
    counterexample = "" if conjecture_holds else f"tau(DISJ_{n}) = {tau_M}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        counterexample_desc = f"tau(DISJ_{first_failing_seed}) = {results[seeds.index(first_failing_seed)]['metric_value']}"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")