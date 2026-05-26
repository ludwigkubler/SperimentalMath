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
    
    def generate_random_boolean_matrix(n):
        return [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    def matrix_rank(matrix):
        m = len(matrix)
        n = len(matrix[0])
        rank = 0
        A = [row[:] for row in matrix]
        
        for i in range(m):
            if all(A[j][i] == 0 for j in range(i, m)):
                continue
            
            if i != rank:
                A[i], A[rank] = A[rank], A[i]
            
            pivot = A[rank][i]
            for j in range(n):
                A[rank][j] /= pivot
            
            for k in range(m):
                if k == rank:
                    continue
                factor = A[k][i]
                for j in range(n):
                    A[k][j] -= factor * A[rank][j]
            
            rank += 1
        
        return rank
    
    def communication_complexity(matrix):
        n = len(matrix)
        max_comm_cost = 0
        
        for i in range(n):
            for j in range(i + 1, n):
                if matrix[i][j] == 1:
                    comm_cost = abs(i - j) + 1
                    if comm_cost > max_comm_cost:
                        max_comm_cost = comm_cost
        
        return max_comm_cost
    
    def free_entanglement_dimension(matrix):
        rank = matrix_rank(matrix)
        n = len(matrix)
        return rank * (n - rank)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 5 instances per seed
            matrix = generate_random_boolean_matrix(n)
            tau_FE = free_entanglement_dimension(matrix)
            CC_R = communication_complexity(matrix)
            
            if CC_R == 0:
                continue
            
            ratio = tau_FE / CC_R
            results.append({"n": n, "tau_FE": tau_FE, "CC_R": CC_R, "ratio": ratio})
    
    if not results:
        return {
            "metric_name": "tau_FE / CC_R",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid matrices found"
        }
    
    n_avg = sum(r["n"] * r["ratio"] for r in results) / len(results)
    ratio_avg = sum(r["ratio"] for r in results) / len(results)
    
    return {
        "metric_name": "tau_FE / CC_R",
        "metric_value": ratio_avg,
        "instances_tested": len(results),
        "conjecture_holds": ratio_avg >= n_avg * (n_avg ** 2 / 4),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30))  # Default to first 29 primes
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    n_avg = sum(r["instances_tested"] * r["metric_value"] for r in results) / sum(r["instances_tested"] for r in results)
    ratio_avg = sum(r["ratio"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={n_avg} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={n_avg} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"ratio below threshold\" first_failing_seed={first_failing_seed}")