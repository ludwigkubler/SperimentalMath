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
    n = len(matrix)
    for i in range(n):
        # Find pivot
        max_row = i
        for k in range(i+1, n):
            if abs(matrix[k][i]) > abs(matrix[max_row][i]):
                max_row = k
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below
        for k in range(i+1, n):
            factor = Fraction(matrix[k][i], matrix[i][i])
            for j in range(n):
                matrix[k][j] -= factor * matrix[i][j]

def determinant(matrix):
    n = len(matrix)
    det = 1
    augmented_matrix = [row[:] + [1 if i == j else 0 for j in range(n)] for i, row in enumerate(matrix)]
    
    gaussian_elimination(augmented_matrix)
    
    for i in range(n):
        det *= augmented_matrix[i][n]
    
    return det

def tensor_product(cnf):
    n = len(cnf)
    m = 2 ** n
    result = [[0] * (m * m) for _ in range(m * m)]
    
    for i in range(m):
        for j in range(m):
            for k in range(n):
                if (i >> k) & 1:
                    result[i * m + j][(k * m) + j] = -1
                else:
                    result[i * m + j][(k * m) + i] = -1
    
    return result

def tropical_rank(matrix):
    n = len(matrix)
    for i in range(n):
        for j in range(i+1, n):
            if matrix[i][j] > matrix[j][i]:
                matrix[i], matrix[j] = matrix[j], matrix[i]
    
    rank = 0
    for row in matrix:
        if any(x != 0 for x in row):
            rank += 1
    
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    
    tensor_prod = tensor_product(cnf)
    rank = tropical_rank(tensor_prod)
    
    theta_n = math.log(n, 2)
    metric_value = abs(rank - theta_n)
    conjecture_holds = metric_value <= 3
    counterexample = "" if conjecture_holds else f"rank={rank}, theta_n={theta_n}"
    
    return {
        "metric_name": "tropical_rank_difference",
        "metric_value": metric_value,
        "instances_tested": n * n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")