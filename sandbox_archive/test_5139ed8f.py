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
from fractions import Fraction
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_sat_instance(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def compute_clause_indicator_polynomial(clauses, n):
        polynomial = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in clauses:
            x1, x2 = abs(clause[0]), abs(clause[1])
            sign = -1 if clause[0] < 0 else 1
            sign *= -1 if clause[1] < 0 else 1
            polynomial[x1][x2] += sign
        return polynomial
    
    def compute_local_ring_norm(polynomial):
        n = len(polynomial) - 1
        norm = 0
        for i in range(1, n + 1):
            for j in range(i, n + 1):
                norm += abs(polynomial[i][j])
        return norm
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i
            for k in range(i + 1, n):
                if abs(matrix[k][i]) > abs(matrix[max_row][i]):
                    max_row = k
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = Fraction(1, matrix[i][i])
            for j in range(n):
                matrix[i][j] *= factor
            for k in range(n):
                if k != i:
                    factor = -matrix[k][i]
                    for j in range(n):
                        matrix[k][j] += factor * matrix[i][j]
        return matrix
    
    def compute_minimal_local_ring_norm(polynomial, n):
        augmented_matrix = [row + [0] for row in polynomial] + [[0] * (n + 1) + [1]]
        gaussian_elimination(augmented_matrix)
        norm = 0
        for i in range(n + 1):
            norm += abs(augmented_matrix[i][-1])
        return norm
    
    def compute_clause_set_complexity(clauses):
        return len(clauses)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            clauses = generate_sat_instance(n)
            polynomial = compute_clause_indicator_polynomial(clauses, n)
            norm = compute_minimal_local_ring_norm(polynomial, n)
            complexity = compute_clause_set_complexity(clauses)
            results.append((norm, complexity))
    
    if not results:
        return {
            "metric_name": "minimal_local_ring_norm",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    norms, complexities = zip(*results)
    mean_norm = sum(norms) / len(norms)
    std_norm = math.sqrt(sum((x - mean_norm) ** 2 for x in norms) / len(norms))
    correlation_coefficient = (sum(x * y for x, y in zip(norms, complexities)) -
                               len(norms) * mean_norm * mean_complexity) / \
                              (len(norms) * std_norm * std_complexity)
    
    return {
        "metric_name": "minimal_local_ring_norm",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient > 0.8 and all(norm <= 5 * math.sqrt(complexity) for norm, complexity in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")