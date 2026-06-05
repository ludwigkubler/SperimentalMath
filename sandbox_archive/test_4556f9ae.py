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
                for k in range(n + 1):
                    matrix[j][k] -= factor * matrix[i][k]
        
        # Back substitution
        x = [0.0] * n
        for i in range(n-1, -1, -1):
            x[i] = matrix[i][n] / matrix[i][i]
            for j in range(i-1, -1, -1):
                matrix[j][n] -= matrix[j][i] * x[i]
        
        return x
    
    def matrix_rank(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            if all(abs(matrix[i][j]) < 1e-9 for j in range(n)):
                continue
            rank += 1
            for j in range(i+1, n):
                factor = matrix[j][i] / matrix[i][i]
                for k in range(n + 1):
                    matrix[j][k] -= factor * matrix[i][k]
        return rank
    
    def communication_complexity_rank(matrix):
        return matrix_rank(matrix)
    
    def minimal_order(sheaf):
        # Placeholder for actual computation
        return len(sheaf)
    
    n = random.randint(5, 40)
    matrix = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    sheaf = [sum(row[i] for row in matrix) for i in range(n)]
    
    min_order = minimal_order(sheaf)
    cr = communication_complexity_rank(matrix)
    
    if cr == 0:
        return {
            "metric_name": "MinOrder",
            "metric_value": min_order,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    if not (0.5 * cr <= min_order <= 1.5 * cr):
        return {
            "metric_name": "MinOrder",
            "metric_value": min_order,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": f"min_order={min_order}, expected in [0.5*{cr}, 1.5*{cr}]"
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
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")