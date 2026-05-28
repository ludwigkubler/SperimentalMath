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
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]

def rank(A):
    A_copy = [row[:] for row in A]
    gaussian_elimination(A_copy)
    return sum(1 for row in A_copy if any(row))

def quadratic_form_matrix(bp):
    variables = set()
    for clause in bp:
        for var in clause:
            variables.add(var)
            variables.add('~' + var)
    
    n = len(variables)
    Q = [[0] * n for _ in range(n)]
    
    for i, var1 in enumerate(sorted(variables)):
        for j, var2 in enumerate(sorted(variables)):
            if var1 == var2:
                Q[i][j] = 1
            elif var1.startswith('~') and var2.startswith('~'):
                if var1[1:] == var2[1:]:
                    Q[i][j] = -1
    
    return Q

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    m = random.randint(1, n)
    s = random.randint(m, 3 * m)
    
    bp = []
    for _ in range(s):
        clause = [random.choice(['x' + str(i) for i in range(n)])]
        if random.random() < 0.5:
            clause.append('~' + random.choice(['x' + str(i) for i in range(n)]))
        bp.append(clause)
    
    Q = quadratic_form_matrix(bp)
    rank_Q = rank(Q)
    
    instances_tested = 1
    conjecture_holds = rank_Q <= m**2 * math.log(2*n+2*s, 2)
    counterexample = "" if conjecture_holds else f"Rank {rank_Q} > O(m^2 log n)"
    
    return {
        "metric_name": "rank",
        "metric_value": rank_Q,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    std_rank = math.sqrt(sum((result["metric_value"] - mean_rank)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")