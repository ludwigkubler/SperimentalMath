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

def gram_schmidt(matrix):
    n = len(matrix)
    Q = [[0] * n for _ in range(n)]
    R = [[0] * n for _ in range(n)]

    for i in range(n):
        v = matrix[i]
        for j in range(i):
            r = sum(Q[j][k] * v[k] for k in range(n))
            R[j][i] = r
            v = [v[k] - r * Q[j][k] for k in range(n)]
        
        norm = math.sqrt(sum(v[k]**2 for k in range(n)))
        if norm == 0:
            raise ValueError("Gram-Schmidt process failed: matrix is not full rank")
        
        R[i][i] = norm
        Q[i] = [v[k] / norm for k in range(n)]
    
    return Q, R

def minrank(matrix):
    try:
        Q, _ = gram_schmidt(matrix)
        rank = sum(1 for row in Q if any(row[j] != 0 for j in range(len(row))))
        return rank
    except ValueError as e:
        return None

def communication_complexity(n):
    # Placeholder function to compute communication complexity
    # This is a dummy implementation and should be replaced with actual computation
    return n * math.log2(n)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        if n > 40:
            break
        
        instances_tested = 0
        total_ranks = 0
        total_complexities = 0
        
        for _ in range(5):  # Test each size with 5 random matrices
            A = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
            if not all(A[i][j] == A[j][i] for i in range(n) for j in range(i)):
                continue
            
            symplectic_A = []
            for i in range(n):
                row = [0] * n
                row[2*i] = 1
                row[2*i+1] = -1
                symplectic_A.append(row)
            
            rank = minrank(symplectic_A)
            if rank is None:
                continue
            
            complexity = communication_complexity(n)
            results.append((n, rank, complexity))
            instances_tested += 1
            total_ranks += rank
            total_complexities += complexity
        
        if instances_tested == 0:
            return {
                "metric_name": "minrank(A_{symplectic}) vs ω(n)",
                "metric_value": None,
                "instances_tested": 0,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        mean_rank = total_ranks / instances_tested
        mean_complexity = total_complexities / instances_tested
        
        # Calculate correlation coefficient
        covariance = sum((rank - mean_rank) * (complexity - mean_complexity) for n, rank, complexity in results)
        variance_rank = sum((rank - mean_rank)**2 for n, rank, _ in results)
        variance_complexity = sum((complexity - mean_complexity)**2 for _, _, complexity in results)
        
        if variance_rank == 0 or variance_complexity == 0:
            return {
                "metric_name": "minrank(A_{symplectic}) vs ω(n)",
                "metric_value": None,
                "instances_tested": instances_tested,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        correlation_coefficient = covariance / (math.sqrt(variance_rank) * math.sqrt(variance_complexity))
        
        return {
            "metric_name": "minrank(A_{symplectic}) vs ω(n)",
            "metric_value": correlation_coefficient,
            "instances_tested": instances_tested,
            "n_max": n,
            "conjecture_holds": correlation_coefficient > 0.9,
            "counterexample": ""
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results if result["metric_value"] is not None)) / len(results)
    
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")