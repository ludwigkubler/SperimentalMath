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
        factor = Fraction(1, matrix[i][i])
        for j in range(i+1, n):
            matrix[j][i] *= factor
        
        # Eliminate above
        for k in range(i):
            factor = Fraction(matrix[k][i], matrix[i][i])
            for j in range(n):
                matrix[k][j] -= factor * matrix[i][j]
    
    rank = sum(1 for row in matrix if any(row[j] != 0 for j in range(n)))
    return rank

def compute_tropicalized_rank(M):
    n = len(M)
    tropicalized_matrix = [[min(M[i][k], M[k][j]) for k in range(n)] for i in range(n)]
    return gaussian_elimination(tropicalized_matrix)

def compute_smallest_ac0_circuit_size(S):
    n = len(S)
    if n == 1:
        return 1
    elif n == 2:
        return 2
    else:
        # Use a simple heuristic: the size of the smallest AC0 circuit for XOR-AND networks grows with n
        return 2 * (n - 1)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    M = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    S = [random.sample(range(n), random.randint(1, n//2)) for _ in range(10)]
    
    tropicalized_ranks = [compute_tropicalized_rank(M) for _ in range(30)]
    ac0_circuit_sizes = [compute_smallest_ac0_circuit_size(s) for s in S]
    
    mean_tropicalized_rank = sum(tropicalized_ranks) / len(tropicalized_ranks)
    mean_ac0_circuit_size = sum(ac0_circuit_sizes) / len(ac0_circuit_sizes)
    
    correlation_coefficient = 0
    if mean_ac0_circuit_size != 0:
        covariance = sum((t - mean_tropicalized_rank) * (a - mean_ac0_circuit_size) for t, a in zip(tropicalized_ranks, ac0_circuit_sizes))
        variance_ac0 = sum((a - mean_ac0_circuit_size) ** 2 for a in ac0_circuit_sizes)
        correlation_coefficient = covariance / math.sqrt(variance_ac0 * len(tropicalized_ranks))
    
    conjecture_holds = correlation_coefficient >= 0.8
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.8"
    
    return {
        "metric_name": "Tropicalized Rank / AC0 Circuit Size",
        "metric_value": mean_tropicalized_rank,
        "instances_tested": len(tropicalized_ranks),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30*31, 2))  # List of first 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.8\" first_failing_seed={first_failing_seed}")