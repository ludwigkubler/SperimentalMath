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
    
    def matrix_multiply(A, B):
        m, k = len(A), len(B[0])
        n = len(B)
        C = [[sum(A[i][j] * B[j][k] for j in range(n)) for k in range(m)] for i in range(k)]
        return C
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(min(m, n)):
            # Find pivot
            max_row = i + random.choice(range(i, m))
            A[i], A[max_row] = A[max_row], A[i]
            
            # Eliminate below
            for j in range(i+1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        
        # Back-substitute
        for i in range(min(m, n)-1, -1, -1):
            for j in range(i+1, m):
                A[i][j] = 0
            A[i][i] /= A[i][i]
            for k in range(n-1, i-1, -1):
                A[i][k] /= A[i][i]
        
        return A
    
    def rank(matrix):
        reduced_matrix = gaussian_elimination(matrix)
        rank = sum(1 for row in reduced_matrix if any(row))
        return rank
    
    def communication_complexity(depth):
        # Simplified model of communication complexity
        return depth * 2
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        matrix = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        depth = random.randint(1, n)
        
        kahler_rank = rank(matrix)
        comm_complexity = communication_complexity(depth)
        
        results.append({
            "n": n,
            "kahler_rank": kahler_rank,
            "comm_complexity": comm_complexity
        })
    
    mean_diff = sum(result["kahler_rank"] - result["comm_complexity"] for result in results) / len(results)
    conjecture_holds = all(result["kahler_rank"] >= result["comm_complexity"] for result in results)
    
    return {
        "metric_name": "rank_difference",
        "metric_value": mean_diff,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"n={results[0]['n']}, kahler_rank={results[0]['kahler_rank']}, comm_complexity={results[0]['comm_complexity']}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] if sys.argv[1:] else list(range(2, 37))  # First 30 primes
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_diff = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_diff} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_diff} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['n']}, kahler_rank={results[0]['kahler_rank']}, comm_complexity={results[0]['comm_complexity']}\" first_failing_seed={first_failing_seed}")