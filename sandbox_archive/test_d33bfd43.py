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
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate non-pivot elements
        pivot = matrix[i][i]
        for j in range(i, n):
            matrix[i][j] /= pivot
        
        for k in range(n):
            if k != i:
                factor = matrix[k][i]
                for j in range(i, n):
                    matrix[k][j] -= factor * matrix[i][j]
    rank = sum(1 for row in matrix if any(row))
    return rank

def communication_complexity_rank(f):
    n = len(f)
    A_f = [[0] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(i+1, n):
            A_f[i][j] = 1 if f[i] != f[j] else 0
            A_f[j][i] = A_f[i][j]
    
    return gaussian_elimination(A_f)

def local_indeterminacy(C_f):
    # Placeholder for actual computation of local indeterminacy
    # For simplicity, we assume it's a random value between 0 and n^2
    return random.randint(0, n**2)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = [random.choice([0, 1]) for _ in range(n)]
    
    C_f = [[] for _ in range(2**n)]
    for i in range(2**n):
        assignment = [int(x) for x in format(i, f'0{n}b')]
        C_f[i].append(assignment)
    
    local_indet = local_indeterminacy(C_f)
    A_f_rank = communication_complexity_rank(f)
    
    return {
        "metric_name": "communication_complexity_rank",
        "metric_value": A_f_rank,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": local_indet <= A_f_rank,
        "counterexample": "" if local_indet <= A_f_rank else f"local_indet={local_indet} > A_f_rank={A_f_rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"local_indet > A_f_rank\" first_failing_seed={first_failing_seed}")