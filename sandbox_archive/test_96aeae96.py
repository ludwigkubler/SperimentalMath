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
    
    def construct_sheaf(f):
        n = len(f)
        sheaf = []
        for i in range(n):
            row = [f[j] if j & (1 << i) else 0 for j in range(2**n)]
            sheaf.append(row)
        return sheaf
    
    def min_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(m):
            max_row = -1
            for j in range(i, m):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            if matrix[max_row][i] == 0:
                continue
            rank += 1
            for j in range(n):
                matrix[i][j], matrix[max_row][j] = matrix[max_row][j], matrix[i][j]
            for k in range(m):
                if k != i:
                    factor = -matrix[k][i] / matrix[i][i]
                    for j in range(n):
                        matrix[k][j] += factor * matrix[i][j]
        return rank
    
    def acc0_circuit_weight(f):
        n = len(f)
        weight = 0
        for i in range(1, n):
            if f[i] != f[0]:
                weight += 1
        return weight
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = [random.choice([0, 1]) for _ in range(2**n)]
        sheaf = construct_sheaf(f)
        rank = min_rank(sheaf)
        weight = acc0_circuit_weight(f)
        
        if rank < math.log(n) or rank > 2 * math.log(n):
            return {
                "metric_name": "minimal_rank",
                "metric_value": rank,
                "instances_tested": len(n_values),
                "conjecture_holds": False,
                "counterexample": f"n={n}, minimal_rank={rank}"
            }
        
        results.append((rank, weight))
    
    mean_rank = sum(rank for rank, _ in results) / len(results)
    std_rank = math.sqrt(sum((rank - mean_rank)**2 for rank, _ in results) / len(results))
    support_fraction = all(math.log(n) <= rank <= 2 * math.log(n) for n, rank in results)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_rank,
        "instances_tested": len(n_values),
        "conjecture_holds": support_fraction,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30))  # Default to first 30 primes
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    std_rank = math.sqrt(sum((result["metric_value"] - mean_rank)**2 for result in results) / len(results))
    support_fraction = all(result["conjecture_holds"] for result in results)
    
    if support_fraction:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"minimal_rank outside bounds\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")