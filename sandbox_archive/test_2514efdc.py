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
    n = len(matrix)
    for i in range(n):
        # Find pivot row
        max_row = i
        for k in range(i+1, n):
            if abs(matrix[k][i]) > abs(matrix[max_row][i]):
                max_row = k
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate non-pivot elements below the pivot
        denom = matrix[i][i]
        for j in range(i, n):
            matrix[i][j] /= denom
        
        for k in range(i+1, n):
            factor = matrix[k][i]
            for j in range(i, n):
                matrix[k][j] -= factor * matrix[i][j]
    
    # Count non-zero rows
    rank = 0
    for i in range(n):
        if any(matrix[i]):
            rank += 1
    return rank

def min_rank_tropical_lie_algebra(cnf):
    n = len(cnf)
    A = [[0] * n for _ in range(n)]
    
    # Fill the matrix with tropicalized values
    for i in range(n):
        for j in range(i+1, n):
            if cnf[i][j]:
                A[i][j] = 1
                A[j][i] = 1
    
    return gaussian_elimination(A)

def weight_disjunctive_normal_form(cnf):
    # Placeholder function to compute the weight of the smallest DNF circuit
    # This is a dummy implementation and should be replaced with actual logic
    return len(cnf) * len(cnf[0])

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    cnf = [[random.choice([True, False]) for _ in range(n)] for _ in range(n)]
    
    min_rank = min_rank_tropical_lie_algebra(cnf)
    weight_dnf = weight_disjunctive_normal_form(cnf)
    
    return {
        "metric_name": "min_rank",
        "metric_value": min_rank,
        "instances_tested": 1,
        "conjecture_holds": min_rank == weight_dnf,
        "counterexample": "" if min_rank == weight_dnf else f"Instance with n={n}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30*100 + 1, 100))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Instance with n={len(results[0]['counterexample'])}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")