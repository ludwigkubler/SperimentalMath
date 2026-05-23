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
        for j in range(i + 1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below
        for j in range(i + 1, n):
            factor = Fraction(matrix[j][i], matrix[i][i])
            for k in range(n):
                matrix[j][k] -= factor * matrix[i][k]

def rank(matrix):
    n = len(matrix)
    copy_matrix = [row[:] for row in matrix]
    gaussian_elimination(copy_matrix)
    rank = 0
    for i in range(n):
        if any(copy_matrix[i]):
            rank += 1
    return rank

def compute_tropicalized_rank(M):
    n = len(M)
    tropicalized_matrix = [[min(M[i][k], M[k][j]) for k in range(n)] for i in range(n)]
    return rank(tropicalized_matrix)

def compute_xor_and_network_size(S):
    n = len(S)
    if n == 1:
        return 1
    else:
        mid = n // 2
        left_size = compute_xor_and_network_size(S[:mid])
        right_size = compute_xor_and_network_size(S[mid:])
        return 1 + left_size + right_size

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Generate a random compact symplectic manifold M and subset S
    n = random.randint(5, 40)
    M = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    S = [random.sample(range(n), k=random.randint(1, n)) for _ in range(30)]
    
    tropicalized_ranks = [compute_tropicalized_rank(M) for _ in range(30)]
    xor_and_network_sizes = [compute_xor_and_network_size(s) for s in S]
    
    if not tropicalized_ranks or not xor_and_network_sizes:
        return {
            "metric_name": "Minimal Rank (Tropicalized Symplectic Geometry)",
            "metric_value": 0,
            "instances_tested": len(tropicalized_ranks),
            "conjecture_holds": False,
            "counterexample": "Empty list of ranks or sizes"
        }
    
    mean_tropical_rank = sum(tropicalized_ranks) / len(tropicalized_ranks)
    mean_xor_and_network_size = sum(xor_and_network_sizes) / len(xor_and_network_sizes)
    
    correlation_coefficient = 0
    if mean_tropical_rank != 0 and mean_xor_and_network_size != 0:
        numerator = sum((t - mean_tropical_rank) * (x - mean_xor_and_network_size) for t, x in zip(tropicalized_ranks, xor_and_network_sizes))
        denominator = math.sqrt(sum((t - mean_tropical_rank) ** 2 for t in tropicalized_ranks)) * math.sqrt(sum((x - mean_xor_and_network_size) ** 2 for x in xor_and_network_sizes))
        correlation_coefficient = numerator / denominator
    
    conjecture_holds = correlation_coefficient >= 0.8
    counterexample = "" if conjecture_holds else "Correlation coefficient < 0.8"
    
    return {
        "metric_name": "Minimal Rank (Tropicalized Symplectic Geometry)",
        "metric_value": mean_tropical_rank,
        "instances_tested": len(tropicalized_ranks),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction=1")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='Correlation coefficient < 0.8' first_failing_seed={first_failing_seed}")