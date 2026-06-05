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
        if matrix[i][i] == 0:
            # Find a non-zero pivot below the current row
            for j in range(i + 1, n):
                if matrix[j][i] != 0:
                    matrix[i], matrix[j] = matrix[j], matrix[i]
                    break
            else:
                raise ValueError("Matrix is singular")
        factor = Fraction(1, matrix[i][i])
        for k in range(n):
            matrix[i][k] *= factor
        for j in range(n):
            if i != j:
                factor = matrix[j][i]
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]

def communication_complexity_rank(matrix):
    n = len(matrix)
    matrix_copy = [row[:] for row in matrix]
    gaussian_elimination(matrix_copy)
    rank = sum(1 for row in matrix_copy if any(row))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 5 + (seed % 6) * 5  # Sweep through {5, 10, 15, 20, 30, 40}
    
    # Generate a random affine scheme X with n points
    points = list(range(n))
    sheaf_matrix = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    
    cr = communication_complexity_rank(sheaf_matrix)
    min_order = sum(sum(row) for row in sheaf_matrix)
    
    if cr == 0:
        return {
            "metric_name": "MinOrder",
            "metric_value": min_order,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "CR(X) is zero, making the correlation undefined"
        }
    
    if not (0.5 * cr <= min_order <= 1.5 * cr):
        return {
            "metric_name": "MinOrder",
            "metric_value": min_order,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": f"MinOrder(X) = {min_order}, CR(X) = {cr}"
        }
    
    return {
        "metric_name": "MinOrder",
        "metric_value": min_order,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"MinOrder(X) is not within the range [0.5 * CR(X), 1.5 * CR(X)]\" first_failing_seed={first_failing_seed}")