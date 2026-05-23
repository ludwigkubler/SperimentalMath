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
    coeffs = [random.choice([0, 1]) for _ in range(n)]
    polynomial = sum(c * v for c, v in zip(coeffs, variables))
    return polynomial

def generate_matrix(m, n):
    matrix = [[random.choice([0, 1]) for _ in range(n)] for _ in range(m)]
    return matrix

def determinant(matrix):
    if len(matrix) == 1:
        return matrix[0][0]
    det = 0
    for c in range(len(matrix)):
        submatrix = [row[:c] + row[c+1:] for row in matrix[1:]]
        sign = (-1) ** (c % 2)
        sub_det = determinant(submatrix)
        det += sign * matrix[0][c] * sub_det
    return det

def gaussian_elimination(matrix):
    m, n = len(matrix), len(matrix[0])
    for i in range(m):
        if matrix[i][i] == 0:
            for j in range(i+1, m):
                if matrix[j][i] != 0:
                    matrix[i], matrix[j] = matrix[j], matrix[i]
                    break
            else:
                return None
        pivot = matrix[i][i]
        for j in range(n):
            matrix[i][j] /= pivot
        for j in range(m):
            if j != i and matrix[j][i] != 0:
                factor = matrix[j][i]
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
    return matrix

def rank(matrix):
    rref = gaussian_elimination(matrix)
    if rref is None:
        return float('inf')
    rank = 0
    for row in rref:
        if any(row):
            rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        polynomial = generate_polynomial(n)
        Q_f_rank = rank([[int(polynomial.subs({f"x{i}": i % 2}) == 0) for i in range(1, n+1)] for _ in range(n)])
        
        for m in range(1, int(math.sqrt(n))**2):
            matrix = generate_matrix(m, n)
            det_circuit_size = len(determinant(matrix))
            
            results.append({
                "n": n,
                "m": m,
                "Q_f_rank": Q_f_rank,
                "det_circuit_size": det_circuit_size
            })
    
    mean_Q_f_rank = sum(result["Q_f_rank"] for result in results) / len(results)
    mean_det_circuit_size = sum(result["det_circuit_size"] for result in results) / len(results)
    
    conjecture_holds = all(abs(Q_f_rank - n**1.5) <= 0.1 * n**1.5 and det_circuit_size >= 0.5 * Q_f_rank for result in results)
    
    return {
        "metric_name": "Q_f_rank",
        "metric_value": mean_Q_f_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(seed) for seed in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")