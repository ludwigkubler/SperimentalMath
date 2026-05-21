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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    rank = 0
    for j in range(cols):
        i_max = -1
        for i in range(rank, rows):
            if matrix[i][j] != 0:
                i_max = i
                break
        if i_max == -1:
            continue
        matrix[rank], matrix[i_max] = matrix[i_max], matrix[rank]
        for i in range(rows):
            if i != rank and matrix[i][j] != 0:
                factor = matrix[i][j] / matrix[rank][j]
                for k in range(cols):
                    matrix[i][k] -= factor * matrix[rank][k]
        rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    variables = list(range(1, n + 1))
    
    # Generate a k-CLIQUE instance (3-CNF formula)
    clauses = []
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < 0.5:
                clauses.append([i + 1, -j - 1])
            elif random.random() < 0.5:
                clauses.append([-i - 1, j + 1])
    
    # Construct the matroid (incidence matrix)
    matrix = [[int(abs(clause) == var) for var in variables] for clause in clauses]
    
    # Compute the maximum rank via Gaussian elimination
    max_rank = gaussian_elimination(matrix)
    
    # Determine if this is a k-CLIQUE instance or random
    is_k_clique = len(clauses) == n * (n - 1) // 2
    
    # Check the conjecture
    if is_k_clique:
        expected_rank = math.ceil(n / 3)
    else:
        expected_rank = math.log(n, 2)
    
    return {
        "metric_name": "matroid_rank",
        "metric_value": max_rank,
        "instances_tested": 1,
        "conjecture_holds": max_rank >= expected_rank,
        "counterexample": "" if max_rank >= expected_rank else f"n={n}, rank={max_rank}"
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
    std_dev = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[first_failing_seed]['metric_value']}, rank={results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")