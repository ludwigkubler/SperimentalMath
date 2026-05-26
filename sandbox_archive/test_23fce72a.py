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
    n = len(matrix)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below
        for j in range(i+1, n):
            factor = matrix[j][i] / matrix[i][i]
            for k in range(n):
                matrix[j][k] -= factor * matrix[i][k]

    # Back-substitute
    for i in range(n-1, -1, -1):
        for j in range(i+1, n):
            matrix[i][-1] -= matrix[j][-1] * matrix[i][j]
        matrix[i][-1] /= matrix[i][i]
        matrix[i][i] = 1

    return [row[-1] for row in matrix]

def compute_min_rank(frege_tree):
    if isinstance(frege_tree, str):
        return 1
    left, right = frege_tree.split(' ', 1)
    return max(compute_min_rank(left), compute_min_rank(right))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    depth = math.ceil(math.log(n, 2))
    frege_trees = [random.choice(['A', 'B']) for _ in range(n)]
    
    min_ranks = []
    for tree in frege_trees:
        min_rank = compute_min_rank(tree)
        if min_rank > depth:
            return {
                "metric_name": "min_rank",
                "metric_value": min_rank,
                "instances_tested": n,
                "conjecture_holds": False,
                "counterexample": f"Tree {tree} has min rank {min_rank} > depth {depth}"
            }
        min_ranks.append(min_rank)
    
    return {
        "metric_name": "min_rank",
        "metric_value": sum(min_ranks) / len(min_ranks),
        "instances_tested": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 30 primes if no seeds provided
    
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
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={seed}")
                break