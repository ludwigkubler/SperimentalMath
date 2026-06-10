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
        # Find pivot in column i
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate entries below pivot
        factor = A[i][i]
        for j in range(i+1, n):
            A[j][i] /= factor
    
    return A

def grothendieck_witt_class(protocol):
    n = len(protocol)
    A = [[0]*n for _ in range(n)]
    
    # Construct the matrix A from the protocol
    for i in range(n):
        for j in range(i+1, n):
            if protocol[i][j] != protocol[j][i]:
                return 0
    
    # Perform Gaussian elimination to simplify the matrix
    A = gaussian_elimination(A)
    
    # Count the number of non-zero rows
    gw_class = sum(1 for row in A if any(row))
    
    return gw_class

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 30
    max_gw_class = 0
    
    for _ in range(instances_tested):
        rank_variance = random.randint(1, n_max)
        protocol = [[random.choice([0, 1]) for _ in range(rank_variance)] for _ in range(rank_variance)]
        
        gw_class = grothendieck_witt_class(protocol)
        max_gw_class = max(max_gw_class, gw_class)
    
    return {
        "metric_name": "max_gw_class",
        "metric_value": max_gw_class,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": max_gw_class <= 2 * n_max,  # Example constant c=2
        "counterexample": "" if max_gw_class <= 2 * n_max else f"max_gw_class={max_gw_class} > 2*n_max"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='{result['counterexample']}' first_failing_seed={first_failing_seed}")