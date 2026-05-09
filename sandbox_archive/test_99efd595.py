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
            factor = matrix[j][i] / matrix[i][i]
            for k in range(n):
                matrix[j][k] -= factor * matrix[i][k]

    rank = sum(1 for row in matrix if any(row))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 40
    alpha_values = [0.5, 1, 1.5]
    results = []
    
    for alpha in alpha_values:
        m = int(n ** alpha)
        matrix = [[random.choice([0, 1]) for _ in range(n)] for _ in range(m)]
        
        rank = gaussian_elimination(matrix)
        results.append((alpha, m, rank))
    
    # Check k-CLIQUE instance
    k = math.ceil(2 * math.sqrt(n))
    clique_matrix = [[1 if i & (1 << j) else 0 for j in range(k)] for i in range(1 << k)]
    k_clique_rank = gaussian_elimination(clique_matrix)
    
    # Analyze results
    sparse_ranks = [rank for alpha, m, rank in results if alpha < 1]
    dense_rank = k_clique_rank
    
    conjecture_holds = all(rank <= math.log(n) for rank in sparse_ranks) and dense_rank >= n
    counterexample = "" if conjecture_holds else "k-CLIQUE instance does not meet the expected rank"
    
    return {
        "metric_name": "Matroid Rank",
        "metric_value": (sum(sparse_ranks) + dense_rank) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")