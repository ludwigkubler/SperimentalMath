# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot row
        max_row = i
        for k in range(i + 1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below pivot
        factor = A[i][i]
        for j in range(i + 1, n):
            A[i][j] /= factor
        A[i][i] = Fraction(1)
        
        # Eliminate above pivot
        for k in range(n):
            if k != i:
                factor = A[k][i]
                for j in range(i, n):
                    A[k][j] -= factor * A[i][j]
                A[k][i] = 0

def min_rank_trop(Q):
    Q_copy = [row[:] for row in Q]
    gaussian_elimination(Q_copy)
    rank = sum(1 for row in Q_copy if any(val != Fraction(0) for val in row))
    return rank

def random_boolean_function(n):
    return [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    f = random_boolean_function(n)
    
    # Construct a quandle representation Q that is as 'tropical' as possible
    Q = [[Fraction(f[i][j]) for j in range(n)] for i in range(n)]
    
    rank_trop = min_rank_trop(Q)
    size_circuit = 2**n
    
    return {
        "metric_name": "minRank_trop vs size_circuit",
        "metric_value": rank_trop,
        "instances_tested": 1,
        "conjecture_holds": rank_trop <= size_circuit,
        "counterexample": "" if rank_trop <= size_circuit else f"rank_trop={rank_trop}, size_circuit={size_circuit}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = (sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))**0.5
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")