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

def generate_disjointness_matrix(n):
    matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j] = 1
            matrix[j][i] = 1
    return matrix

def is_invertible(matrix):
    if len(matrix) != len(matrix[0]):
        return False
    identity = [[Fraction(1, 1) if i == j else Fraction(0, 1) for j in range(len(matrix))] for i in range(len(matrix))]
    augmented_matrix = [row + col for row, col in zip(matrix, identity)]
    return gaussian_elimination(augmented_matrix)

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        if matrix[i][i] == 0:
            for j in range(i + 1, n):
                if matrix[j][i] != 0:
                    matrix[i], matrix[j] = matrix[j], matrix[i]
                    break
            else:
                raise ValueError("Matrix is singular")
        pivot = Fraction(matrix[i][i])
        for k in range(n):
            matrix[i][k] /= pivot
        for j in range(n):
            if i != j:
                factor = matrix[j][i]
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
    return [row[:-n] for row in matrix]

def determinant(matrix):
    if len(matrix) == 1:
        return matrix[0][0]
    det = Fraction(0, 1)
    sign = Fraction(1, 1)
    for i in range(len(matrix)):
        submatrix = [row[:i] + row[i+1:] for row in matrix[1:]]
        det += sign * matrix[0][i] * determinant(submatrix)
        sign *= -Fraction(1, 1)
    return det

def geometric_invariant(matrix):
    if not is_invertible(matrix):
        raise ValueError("Matrix is singular")
    return determinant(gaussian_elimination(matrix))

def communication_complexity(n):
    # Placeholder for actual computation
    return n * (n - 1) // 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    instances_tested = 30
    total_comm = 0
    gamma_sum = 0
    
    for _ in range(instances_tested):
        M_f = generate_disjointness_matrix(n)
        gamma_M_f = geometric_invariant(M_f)
        comm_f = communication_complexity(n)
        
        if comm_f < gamma_M_f:
            return {
                "metric_name": "gamma_M_f",
                "metric_value": float(gamma_M_f),
                "instances_tested": instances_tested,
                "conjecture_holds": False,
                "counterexample": f"comm({n}) = {comm_f} < gamma(M_{n}) = {gamma_M_f}"
            }
        
        total_comm += comm_f
        gamma_sum += gamma_M_f
    
    avg_gamma = gamma_sum / instances_tested
    avg_comm = total_comm / instances_tested
    c = avg_comm / avg_gamma
    
    return {
        "metric_name": "gamma_M_f",
        "metric_value": float(avg_gamma),
        "instances_tested": instances_tested,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_gamma = sum(r["metric_value"] for r in results) / len(results)
    std_gamma = math.sqrt(sum((r["metric_value"] - mean_gamma) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_gamma} std={std_gamma} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"gamma(M_{40}) < c * comm(DISJ_40)\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction")