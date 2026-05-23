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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def free_convolution_matrix(f):
        n = len(f)
        M = [[0] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(2**n):
                M[i][j] = sum(f[k] * f[(i ^ j) ^ k] for k in range(n)) / 2**(n-1)
        return M
    
    def min_rank(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            if all(matrix[j][i] == 0 for j in range(i, n)):
                continue
            pivot_row = next(j for j in range(i, n) if matrix[j][i] != 0)
            if pivot_row != i:
                matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
            rank += 1
            for j in range(n):
                if j == i:
                    continue
                factor = -matrix[j][i] / matrix[i][i]
                for k in range(n):
                    matrix[j][k] += factor * matrix[i][k]
        return rank
    
    def bp_readtwice_width(f):
        n = len(f)
        width = 0
        for i in range(2**n):
            if f[i] == 1:
                width += 1
        return width
    
    results = []
    for _ in range(30):  # Ensure at least 30 instances per seed
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_boolean_function(n)
        M = free_convolution_matrix(f)
        rank = min_rank(M)
        bp_width = bp_readtwice_width(f)
        
        results.append({
            "n": n,
            "rank": rank,
            "bp_width": bp_width
        })
    
    mean_rank = sum(result["rank"] for result in results) / len(results)
    std_rank = math.sqrt(sum((result["rank"] - mean_rank)**2 for result in results) / len(results))
    mean_bp_width = sum(result["bp_width"] for result in results) / len(results)
    
    conjecture_holds = all(abs(rank - math.sqrt(n)) <= 0.1 * math.sqrt(n) for result in results)
    bp_readtwice_supports = all(bp_width <= 2 for result in results)
    
    if not conjecture_holds:
        counterexample = "rank does not follow Θ(n^0.5)"
    elif not bp_readtwice_supports:
        counterexample = "BP_ReadTwice width exceeds 2"
    else:
        counterexample = ""
    
    return {
        "metric_name": "min_rank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    std_rank = math.sqrt(sum((result["metric_value"] - mean_rank)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank does not follow Θ(n^0.5)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")