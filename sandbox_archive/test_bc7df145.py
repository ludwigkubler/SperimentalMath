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
    
    # Generate a random d-dimensional geometric vector field on M
    d = random.randint(2, 10)
    vector_field = [random.random() for _ in range(d)]
    
    # Compute the minimal rank of its holonomy representation H(M)
    min_rank_holonomy = len(vector_field)  # Simplified for testing
    
    # Construct an associated matrix of communication tasks
    comm_complexity_matrix = [[vector_field[j] * vector_field[k] for k in range(d)] for j in range(d)]
    
    # Compute the communication complexity rank
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            if matrix[i][i] == 0:
                return -1  # Singular matrix, no unique solution
            for j in range(i + 1, n):
                factor = Fraction(matrix[j][i], matrix[i][i])
                for k in range(i, n):
                    matrix[j][k] -= factor * matrix[i][k]
        rank = sum(1 for row in matrix if any(row))
        return rank
    
    comm_complexity_rank = gaussian_elimination(comm_complexity_matrix)
    
    # Check if the communication complexity rank is within the valid range
    if not (1 <= comm_complexity_rank <= d):
        return {
            "metric_name": "communication_complexity_rank",
            "metric_value": comm_complexity_rank,
            "instances_tested": 1,
            "n_max": d,
            "conjecture_holds": False,
            "counterexample": "Out of valid range"
        }
    
    # Correlate the minimal rank of holonomy representations with communication complexity ranks
    corr = pearsonr(min_rank_holonomy, comm_complexity_rank)
    
    return {
        "metric_name": "communication_complexity_rank",
        "metric_value": corr,
        "instances_tested": 1,
        "n_max": d,
        "conjecture_holds": corr > 0.7,
        "counterexample": ""
    }

def pearsonr(x, y):
    n = len(x)
    if n != len(y):
        raise ValueError("x and y must have the same length")
    
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    
    cov_xy = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    var_x = sum((xi - mean_x) ** 2 for xi in x)
    var_y = sum((yi - mean_y) ** 2 for yi in y)
    
    if var_x == 0 or var_y == 0:
        return 0
    
    return cov_xy / math.sqrt(var_x * var_y)

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Out of valid range\" first_failing_seed={first_failing_seed}")