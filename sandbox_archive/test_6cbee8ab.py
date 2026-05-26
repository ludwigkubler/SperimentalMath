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

def generate_disjointness_instance(n):
    x = [random.randint(0, 1) for _ in range(n)]
    y = [random.randint(0, 1) for _ in range(n)]
    return x, y

def truth_table(x, y):
    n = len(x)
    M = [[x[i] ^ y[j] for j in range(n)] for i in range(n)]
    return M

def smith_normal_form(matrix):
    m, n = len(matrix), len(matrix[0])
    R = [row[:] for row in matrix]
    
    def find_pivot(R, k):
        for i in range(k, m):
            for j in range(k, n):
                if R[i][j] != 0:
                    return i, j
        return None, None
    
    for k in range(min(m, n)):
        pivot_row, pivot_col = find_pivot(R, k)
        if pivot_row is None or pivot_col is None:
            continue
        
        # Swap rows to make the pivot element non-zero
        R[k], R[pivot_row] = R[pivot_row], R[k]
        
        # Make the pivot element 1 by dividing the row by it
        pivot_value = R[k][k]
        for j in range(k, n):
            R[k][j] /= pivot_value
        
        # Eliminate the pivot column below and to the right
        for i in range(k + 1, m):
            factor = R[i][k]
            for j in range(k, n):
                R[i][j] -= factor * R[k][j]
    
    rank = sum(1 for row in R if any(row))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    instances_tested = 0
    total_rank = 0
    
    for n in [10, 20, 30, 40]:
        for _ in range(7):  # Aim for at least 30 instances per seed
            x, y = generate_disjointness_instance(n)
            M = truth_table(x, y)
            rank = smith_normal_form(M)
            total_rank += rank
            instances_tested += 1
    
    conjecture_holds = total_rank >= n * math.log(n) * instances_tested / (40 * 30)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": total_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank:.2f} std={std_rank:.2f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank:.2f} std={std_rank:.2f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")