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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_density_matrix(f):
        n = int(math.log2(len(f)))
        rho = [[0] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(2**n):
                if f[i] == f[j]:
                    rho[i][j] = 1 / len(f)
        return rho
    
    def matrix_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(min(m, n)):
            if any(matrix[j][i] != 0 for j in range(i, m)):
                rank += 1
                for j in range(i + 1, m):
                    factor = matrix[j][i] / matrix[i][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        return rank
    
    def circuit_weight(f):
        n = int(math.log2(len(f)))
        # Simplified heuristic for circuit weight
        return 2**n
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        rho = compute_density_matrix(f)
        rank = matrix_rank(rho)
        weight = circuit_weight(f)
        
        if rank == 0 or math.log2(len(f)) <= 0:
            continue
        
        results.append({
            "n": n,
            "rank": rank,
            "weight": weight
        })
    
    if not results:
        return {
            "metric_name": "Rank and Weight",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    
    total_rank = sum(result["rank"] for result in results)
    avg_rank = total_rank / len(results)
    max_weight = max(result["weight"] for result in results)
    
    return {
        "metric_name": "Rank and Weight",
        "metric_value": avg_rank,
        "instances_tested": len(results),
        "conjecture_holds": abs(avg_rank - math.log(len(results), 2)) <= 3 * math.log(len(results), 2) / len(results) and max_weight <= 2**avg_rank,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    avg_rank = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - avg_rank)**2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={avg_rank} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")