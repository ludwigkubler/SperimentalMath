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
        # Find pivot in column i with maximum absolute value
        max_row = i
        for k in range(i+1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        A[i], A[max_row] = A[max_row], A[i]
        
        # Make all entries below pivot zero
        for k in range(i+1, n):
            factor = Fraction(A[k][i], A[i][i])
            for j in range(i, n):
                A[k][j] -= factor * A[i][j]

    # Back substitution to find solution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = Fraction(A[i][-1], A[i][i])
        for k in range(i-1, -1, -1):
            A[k][-1] -= A[k][i] * x[i]
    return x

def hodge_rank(matrix):
    n = len(matrix)
    A_copy = [row[:] for row in matrix]
    rank = gaussian_elimination(A_copy)
    return sum(1 for x in rank if x != 0)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        formula = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        lidb_value = hodge_rank(formula)
        hodge_rank_value = hodge_rank(formula)
        
        if lidb_value == 0 or hodge_rank_value == 0:
            continue
        
        results.append((lidb_value, hodge_rank_value))
    
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    lidb_values, hodge_rank_values = zip(*results)
    mean_lidb = sum(lidb_values) / len(lidb_values)
    mean_hodge_rank = sum(hodge_rank_values) / len(hodge_rank_values)
    
    correlation = 0
    for i in range(len(results)):
        correlation += (lidb_values[i] - mean_lidb) * (hodge_rank_values[i] - mean_hodge_rank)
    correlation /= (len(results) * math.sqrt(sum((x - mean_lidb)**2 for x in lidb_values)) * math.sqrt(sum((y - mean_hodge_rank)**2 for y in hodge_rank_values)))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": 0.5 <= correlation < 0.8,
        "counterexample": "" if 0.5 <= correlation < 0.8 else f"correlation={correlation:.2f}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if 0.5 <= r["metric_value"] < 0.8) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr:.2f} std={0:.2f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation below 0.8\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")