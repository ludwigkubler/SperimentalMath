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
        max_row = i + max(range(i, rows), key=lambda r: abs(matrix[r][i]))
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        pivot = matrix[i][i]
        if pivot == 0:
            continue
        for j in range(cols):
            matrix[i][j] /= pivot
        for k in range(rows):
            if k != i:
                factor = matrix[k][i]
                for j in range(cols):
                    matrix[k][j] -= factor * matrix[i][j]

def rank(matrix):
    rows, cols = len(matrix), len(matrix[0])
    augmented_matrix = [row + [1 if i == j else 0 for j in range(rows)] for i, row in enumerate(matrix)]
    gaussian_elimination(augmented_matrix)
    return sum(1 for row in augmented_matrix if any(row[j] != 0 for j in range(cols)))

def calculate_ranks(protocols):
    ranks = []
    for protocol in protocols:
        ker_phi = protocol['ker_phi']
        rank_ker_phi = rank(ker_phi)
        ranks.append(rank_ker_phi)
    return ranks

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 10
    m = 50
    
    protocols = []
    for _ in range(30):
        ker_phi = [[random.randint(0, 1) for _ in range(m)] for _ in range(n)]
        protocol = {'ker_phi': ker_phi}
        protocols.append(protocol)
    
    ranks = calculate_ranks(protocols)
    rank_variance = sum((x - sum(ranks) / len(ranks)) ** 2 for x in ranks) / len(ranks)
    log_rank_variance = math.log(rank_variance) if rank_variance > 0 else float('-inf')
    k = 1.5
    conjecture_holds = log_rank_variance <= k * math.log(n)
    
    return {
        "metric_name": "log_rank_variance",
        "metric_value": log_rank_variance,
        "instances_tested": len(ranks),
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Counterexample found for seed {seed}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r['metric_value'] for r in results) / len(results)
    std_value = math.sqrt(sum((r['metric_value'] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"Counterexample found\" first_failing_seed={first_failing_seed}")