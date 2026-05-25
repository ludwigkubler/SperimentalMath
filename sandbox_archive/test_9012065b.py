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
    
    def factorial(n):
        if n == 0 or n == 1:
            return 1
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result
    
    def binomial_coefficient(n, k):
        if k > n:
            return 0
        return factorial(n) // (factorial(k) * factorial(n - k))
    
    def determinant(matrix):
        if len(matrix) == 1:
            return matrix[0][0]
        det = 0
        for j in range(len(matrix)):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            sign = (-1) ** j
            det += sign * matrix[0][j] * determinant(submatrix)
        return det
    
    def schur_weyl_rank(n, k):
        if n == 1:
            return 1
        rank = 0
        for i in range(1, n + 1):
            rank += binomial_coefficient(k, i) * (2 ** (n - i))
        return rank
    
    def generate_instance(n, k):
        permutation = list(range(n))
        random.shuffle(permutation)
        instance = [[0] * n for _ in range(n)]
        for i in range(n):
            instance[permutation[i]][i] = 1
        return instance
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        if n < 5 or n > 40:
            continue
        
        k = min(n // 2, 2 ** (n - 1) // 4)
        instance = generate_instance(n, k)
        
        rank = schur_weyl_rank(n, k)
        det = determinant(instance)
        
        if rank == 0 or det == 0:
            continue
        
        ratio = det / rank
        results.append({
            "n": n,
            "k": k,
            "rank": rank,
            "det": det,
            "ratio": ratio
        })
    
    if not results:
        return {
            "metric_name": "Ratio",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }
    
    avg_ratio = sum(result["ratio"] for result in results) / len(results)
    max_ratio = max(result["ratio"] for result in results)
    
    if max_ratio > 1:
        return {
            "metric_name": "Ratio",
            "metric_value": avg_ratio,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": f"Max ratio exceeded: {max_ratio}"
        }
    
    return {
        "metric_name": "Ratio",
        "metric_value": avg_ratio,
        "instances_tested": len(results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_ratio = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        max_counterexample = max((result["counterexample"] for result in results if not result["conjecture_holds"]), key=len)
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{max_counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unreachable")