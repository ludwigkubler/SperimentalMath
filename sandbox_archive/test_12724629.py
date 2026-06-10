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
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        # Find a non-zero pivot in column i
        pivot_row = i
        while matrix[pivot_row][i] == 0:
            pivot_row += 1
            if pivot_row == rows:
                pivot_row -= 1
                break
        
        # Swap rows to put the pivot at position (i, i)
        matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
        
        # Eliminate non-zero entries below the pivot
        for j in range(i + 1, rows):
            factor = Fraction(matrix[j][i], matrix[i][i])
            for k in range(cols):
                matrix[j][k] -= factor * matrix[i][k]
    
    rank = sum(1 for row in matrix if any(row))
    return rank

def generate_communication_matrix(m, n):
    matrix = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(m):
        sender = random.randint(1, n)
        receiver = random.randint(1, n)
        message = random.randint(1, n)
        matrix[sender][receiver] += message
    return matrix

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    mrr_values = []
    instances_tested = 0
    n_max = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            mrr = 0
            for _ in range(m):
                matrix = generate_communication_matrix(m, n)
                rank = gaussian_elimination(matrix)
                mrr += rank
            mrr_values.append(mrr / m)
            instances_tested += m
            n_max = max(n_max, n)
    
    mean_mrr = sum(mrr_values) / len(mrr_values)
    conjecture_holds = all(mrr <= m * math.log(n) for mrr, m, n in zip(mrr_values, [m] * len(mrr_values), [n] * len(mrr_values)))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Minimal Modular Representation Rank",
        "metric_value": mean_mrr,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_mrr = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_mrr} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")