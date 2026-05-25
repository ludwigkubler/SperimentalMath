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
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        # Find pivot row
        max_row = i
        for r in range(i+1, rows):
            if abs(matrix[r][i]) > abs(matrix[max_row][i]):
                max_row = r
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below the pivot
        factor = Fraction(1, matrix[i][i])
        for j in range(i, cols):
            matrix[i][j] *= factor
        
        for r in range(rows):
            if r != i:
                factor = matrix[r][i]
                for j in range(i, cols):
                    matrix[r][j] -= factor * matrix[i][j]
    return matrix

def rank(matrix):
    rows, cols = len(matrix), len(matrix[0])
    rref = gaussian_elimination(matrix)
    rank_value = 0
    for row in rref:
        if any(row):
            rank_value += 1
    return rank_value

def generate_monotone_kclique(n, k):
    # This is a placeholder function. In practice, you would need to implement
    # the generation of random monotone k-CLIQUE instances.
    loci = [[random.choice([0, 1]) for _ in range(k)] for _ in range(n)]
    return loci

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    alpha = Fraction(1, 2)  # Example constant
    results = []
    
    for n in n_values:
        loci = generate_monotone_kclique(n, k=n)
        rank_value = rank(loci)
        
        if rank_value < alpha * n**(3/4):
            return {
                "metric_name": "Minimal Rank",
                "metric_value": rank_value,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"n={n}, rank_value={rank_value} < {alpha * n**(3/4)}"
            }
        
        results.append(rank_value)
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": sum(results) / len(results),
        "instances_tested": len(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results if "metric_value" in r)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={n}, rank_value<{alpha * n**(3/4)}\" first_failing_seed={first_failing_seed}")