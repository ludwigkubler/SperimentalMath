# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations

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
        for j in range(n):
            if i != j:
                factor = Fraction(-matrix[j][i], matrix[i][i])
                for k in range(i, n+1):
                    matrix[j][k] += factor * matrix[i][k]
    
    rank = 0
    for row in matrix:
        if any(row[i] != 0 for i in range(n)):
            rank += 1
    return rank

def construct_polynomial(instance):
    n = len(instance)
    poly = [[0] * (n+1) for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            if instance[i][j]:
                poly[i][j] = 1
                poly[j][i] = 1
    return poly

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    instance = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    poly = construct_polynomial(instance)
    
    rank = gaussian_elimination(poly)
    threshold = n**2
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank > threshold,
        "counterexample": "" if rank > threshold else f"Instance not satisfiable with rank {rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=not_computed support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Instance not satisfiable' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")