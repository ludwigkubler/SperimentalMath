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
        
        # Eliminate below the pivot
        for j in range(i+1, n):
            factor = -A[j][i] / A[i][i]
            for k in range(n + 1):
                A[j][k] += factor * A[i][k]

    rank = n
    for i in range(n):
        if abs(A[i][i]) < 1e-9:
            rank -= 1

    return rank

def matroid_rank(f, n):
    indicator_vectors = [[int(x[i] == j) for i in range(n)] for j in range(2)]
    A = [v + [f(v)] for v in indicator_vectors]
    return gaussian_elimination(A)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = lambda x: sum(x) % 2
        M_f_rank = matroid_rank(f, n)
        
        if M_f_rank < n * math.log(n):
            return {
                "metric_name": "matroid_rank",
                "metric_value": M_f_rank,
                "instances_tested": len(n_values),
                "conjecture_holds": False,
                "counterexample": f"Function with rank {M_f_rank} < {n * math.log(n)}"
            }
        
        results.append(M_f_rank)
    
    mean = sum(results) / len(results)
    std_dev = (sum((x - mean) ** 2 for x in results) / len(results)) ** 0.5
    
    return {
        "metric_name": "matroid_rank",
        "metric_value": mean,
        "instances_tested": len(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean = sum(results) / len(results)
    std_dev = (sum((x - mean) ** 2 for x in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r >= n * math.log(n)) / len(results)
    
    if support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(r < n * math.log(n) for r in results):
        first_failing_seed = seeds[results.index(next(r for r in results if r < n * math.log(n)))]
        print(f"RESULT: FALSIFIED counterexample='rank<{n*math.log(n)}' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")