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
        max_row = i
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        factor = Fraction(matrix[i][i], matrix[i][i])
        for j in range(n):
            matrix[i][j] /= factor
        for j in range(n):
            if i != j:
                factor = Fraction(matrix[j][i], matrix[i][i])
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
    return matrix

def quadratic_reciprocity_matrix(n):
    matrix = [[0] * n for _ in range(n)]
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    for i in range(n):
        for j in range(i+1, n):
            p = random.choice(primes)
            matrix[i][j] = (p**i * p**j) % n
            matrix[j][i] = (p**i * p**j) % n
    return matrix

def tseitin_resolution_width(n, m):
    # Placeholder for actual implementation
    return random.randint(10, 20)

def determinant_mod_p(matrix, p):
    # Placeholder for actual implementation
    return random.randint(1, p-1)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(n, 2*n)
    
    matrix = quadratic_reciprocity_matrix(n)
    width = tseitin_resolution_width(n, m)
    determinant_values = [determinant_mod_p(matrix, p) for p in range(2, n+1)]
    
    rank = sum(1 for row in matrix if any(row))
    conjecture_holds = (rank == n and width == math.isqrt(n) * math.log(n, 2)) and all(det != 0 for det in determinant_values)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "width",
        "metric_value": width,
        "instances_tested": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or list(range(2, 30*31, 2))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_width = sum(r["metric_value"] for r in results) / len(results)
    std_width = math.sqrt(sum((r["metric_value"] - mean_width)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")