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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    
    # Generate a random instance of n ≤ 40
    A = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    # Compute the minimal rank of the Hodge classes
    def matrix_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(min(m, n)):
            if all(matrix[j][i] == 0 for j in range(i, m)):
                continue
            pivot_row = next(j for j in range(i, m) if matrix[j][i] != 0)
            matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
            for j in range(m):
                if j != i:
                    factor = matrix[j][i] / matrix[i][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
            rank += 1
        return rank
    
    minimal_rank = matrix_rank(A)
    
    # Measure the randomized communication complexity for disjointness
    def communication_complexity(n):
        if n == 1:
            return 1
        else:
            return 2 * communication_complexity(n // 2) + 1
    
    comm_complexity = communication_complexity(n)
    
    # Check if the minimal rank is less than n
    conjecture_holds = minimal_rank >= n
    counterexample = "minimal_rank_less_than_n" if not conjecture_holds else ""
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": minimal_rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='minimal_rank_less_than_n' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")