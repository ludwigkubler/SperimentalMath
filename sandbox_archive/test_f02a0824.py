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
    
    n = 20
    G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        G[i][i] = 0
    
    # Construct the moment matrix M_d for Max-CUT SDP relaxation
    d = 3  # Example degree, adjust as needed
    M_d = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if G[i][j] == 1:
                for k in range(d + 1):
                    M_d[i][j] += (i ** k) * (j ** k)
                    M_d[j][i] = M_d[i][j]
    
    # Compute the rank of M_d
    rank_M_d = compute_rank(M_d)
    
    # Check if rank(M_d) >= sqrt(n)
    conjecture_holds = rank_M_d >= math.sqrt(n)
    counterexample = "" if conjecture_holds else f"rank(M_d)={rank_M_d}, sqrt(n)={math.sqrt(n)}"
    
    return {
        "metric_name": "Rank of Moment Matrix M_d",
        "metric_value": rank_M_d,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def compute_rank(matrix):
    n = len(matrix)
    A = [row[:] for row in matrix]
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        rank = 0
        
        for i in range(n):
            max_row = None
            max_val = -1
            
            for j in range(rank, m):
                if abs(A[j][i]) > max_val:
                    max_val = abs(A[j][i])
                    max_row = j
            
            if max_row is not None:
                A[rank], A[max_row] = A[max_row], A[rank]
                
                for j in range(n):
                    if i != j:
                        factor = A[j][i] / A[rank][i]
                        for k in range(i, n):
                            A[j][k] -= factor * A[rank][k]
                
                rank += 1
        
        return rank
    
    return gaussian_elimination(A)

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    total_metric_value = sum(result["metric_value"] for result in results)
    mean_metric_value = total_metric_value / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank(M_d) < sqrt(n)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds tested")