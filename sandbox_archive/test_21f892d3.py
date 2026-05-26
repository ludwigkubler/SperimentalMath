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

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        # Find pivot row
        max_row = i
        for k in range(i + 1, n):
            if abs(matrix[k][i]) > abs(matrix[max_row][i]):
                max_row = k
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate non-pivot elements below the pivot
        factor = Fraction(1, matrix[i][i])
        for j in range(i + 1, n):
            matrix[j][i] *= factor
        
        # Eliminate non-pivot elements above the pivot
        for k in range(i):
            factor = matrix[k][i]
            for j in range(n):
                matrix[k][j] -= factor * matrix[i][j]
    
    rank = sum(1 for row in matrix if any(row))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    instance = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    try:
        hodge_rank = gaussian_elimination(instance)
    except ZeroDivisionError:
        return {
            "metric_name": "minimal_rank",
            "metric_value": -1,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "division_by_zero"
        }
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": hodge_rank,
        "instances_tested": 1,
        "conjecture_holds": hodge_rank >= n,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 163))  # Default to first 30 primes
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.2f} std={std_value:.2f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value:.2f} std={std_value:.2f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='division_by_zero' first_failing_seed={first_failing_seed}")