# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from itertools import combinations

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot
        max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]

def rank_polymatroid(clauses):
    n = len(clauses)
    matrix = [[0] * n for _ in range(n)]
    for i, j in combinations(range(n), 2):
        if any(c[i] and c[j] for c in clauses):
            matrix[i][j] = 1
            matrix[j][i] = 1
    
    gaussian_elimination(matrix)
    rank = sum(1 for row in matrix if any(row))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    clauses = [[random.choice([True, False]) for _ in range(n)] for _ in range(n)]
    
    rank = rank_polymatroid(clauses)
    
    if n == 1:
        expected_rank = 1
    else:
        expected_rank = n
    
    conjecture_holds = rank >= expected_rank
    counterexample = "" if conjecture_holds else "n={}".format(n)
    
    return {
        "metric_name": "polymatroid_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30*37, 143))[:30]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL:", result)
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = (sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print("RESULT: SUPPORTED mean=%.2f std=%.2f support_fraction=%.2f" % (mean_rank, std_rank, support_fraction))
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print("RESULT: FALSIFIED counterexample=\"n=1\" first_failing_seed=%d" % first_failing_seed)
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")