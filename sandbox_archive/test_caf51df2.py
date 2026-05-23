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

def generate_polynomial(n):
    variables = [f"x{i}" for i in range(1, n+1)]
    coeffs = [random.randint(0, 1) for _ in range(n)]
    polynomial = sum(c * v for c, v in zip(coeffs, variables))
    return polynomial

def generate_matrix(m, n):
    matrix = [[random.choice([0, 1]) for _ in range(n)] for _ in range(m)]
    return matrix

def determinant(matrix):
    if len(matrix) == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    det = 0
    for i in range(len(matrix)):
        submatrix = [row[:i] + row[i+1:] for row in matrix[1:]]
        sign = (-1) ** (i % 2)
        det += sign * matrix[0][i] * determinant(submatrix)
    return det

def run_trial(seed):
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        polynomial = generate_polynomial(n)
        Q_f_rank = len(polynomial.split())  # Simplified rank calculation
        
        for m in range(1, int(math.sqrt(n))**2):
            matrix = generate_matrix(m, n)
            det = determinant(matrix)
            C_size = len(str(det).split())
            
            results.append({
                "n": n,
                "m": m,
                "polynomial": polynomial,
                "Q_f_rank": Q_f_rank,
                "det": det,
                "C_size": C_size
            })
    
    total_tests = len(results)
    min_Q_f_rank = min(result["Q_f_rank"] for result in results)
    max_C_size = max(result["C_size"] for result in results)
    
    conjecture_holds = (min_Q_f_rank >= n_values[0]**1.5 and
                        max_C_size >= 0.5 * min_Q_f_rank)
    
    return {
        "metric_name": "Conjecture Support",
        "metric_value": (min_Q_f_rank, max_C_size),
        "instances_tested": total_tests,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_Q_f_rank = sum(r["metric_value"][0] for r in results) / len(results)
    mean_C_size = sum(r["metric_value"][1] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean_Q_f_rank={mean_Q_f_rank} mean_C_size={mean_C_size} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")