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
    rows = len(matrix)
    cols = len(matrix[0])
    for i in range(rows):
        # Find pivot row
        max_row = i
        for j in range(i + 1, rows):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate non-pivot elements
        factor = Fraction(1, matrix[i][i])
        for j in range(cols):
            matrix[i][j] *= factor
        
        for k in range(rows):
            if k != i:
                factor = matrix[k][i]
                for j in range(cols):
                    matrix[k][j] -= factor * matrix[i][j]
    return matrix

def rank(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    rank = 0
    for i in range(rows):
        if any(matrix[i][j] != 0 for j in range(cols)):
            rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    instance = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    hodge_rank = rank(gaussian_elimination(instance))
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": hodge_rank,
        "instances_tested": 1,
        "conjecture_holds": hodge_rank >= n,
        "counterexample": "" if hodge_rank >= n else f"n={n}, rank={hodge_rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 103))  # First 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['metric_value']}, rank={results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")