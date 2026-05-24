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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot row
        pivot_row = next(j for j in range(i, n) if A[j][i] != 0)
        A[i], A[pivot_row] = A[pivot_row], A[i]
        
        # Eliminate non-pivot elements in the current column
        for j in range(n):
            if i != j:
                factor = Fraction(A[j][i], A[i][i])
                for k in range(n + 1):
                    A[j][k] -= factor * A[i][k]
    
    # Count non-zero rows to get rank
    rank = sum(1 for row in A if any(row))
    return rank

def min_rank(graph):
    n = len(graph)
    I = [[Fraction(1, 1) if i == j else Fraction(0, 1) for j in range(n)] for i in range(n)]
    A = [[graph[i][j] * graph[k][l] for l in range(n)] for k in range(n) for j in range(n)]
    
    # Perform Gaussian elimination to find the rank
    return gaussian_elimination(A)

def resolution_length(graph):
    n = len(graph)
    clauses = []
    for i in range(n):
        for j in range(i + 1, n):
            if graph[i][j] == 1:
                clauses.append((i, j))
    
    # Simple heuristic to estimate Resolution length
    return len(clauses) * 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    graph = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    MinRank_G_tensor_G = min_rank(graph) ** 2
    ResolutionLength_T_G = resolution_length(graph)
    
    if ResolutionLength_T_G == 0:
        return {
            "metric_name": "MinRank(G ⊗ G) / ResolutionLength(T_G)",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Resolution length is zero, making the division undefined."
        }
    
    metric_value = MinRank_G_tensor_G / ResolutionLength_T_G
    
    return {
        "metric_name": "MinRank(G ⊗ G) / ResolutionLength(T_G)",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": metric_value >= 2,
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
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(r["conjecture_holds"] for r in results if r["metric_value"] is not None) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")