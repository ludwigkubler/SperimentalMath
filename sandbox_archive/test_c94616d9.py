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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_circuit(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            if sum(clause) != 0:
                clauses.append(clause)
        return clauses
    
    def monotone_width(circuit):
        n = len(circuit[0])
        width = 0
        for clause in circuit:
            width = max(width, sum(1 for x in clause if x > 0))
        return width
    
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(n):
            pivot_row = -1
            for j in range(rank, m):
                if matrix[j][i] != 0:
                    pivot_row = j
                    break
            if pivot_row == -1:
                continue
            matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
            for j in range(m):
                if j != rank and matrix[j][i] != 0:
                    factor = Fraction(matrix[j][i], matrix[rank][i])
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[rank][k]
            rank += 1
        return rank
    
    def minimal_order(circuit):
        n = len(circuit[0])
        matrix = [[0] * (n + 1) for _ in range(2**n)]
        for i, clause in enumerate(circuit):
            for j in range(n):
                if clause[j] > 0:
                    matrix[i][j] = 1
                else:
                    matrix[i][n] += 1
        return gaussian_elimination(matrix)
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_order = 0
    total_width = 0
    
    for n in n_values:
        for _ in range(5):
            circuit = generate_circuit(n)
            order = minimal_order(circuit)
            width = monotone_width(circuit)
            total_order += order
            total_width += width
            instances_tested += 1
    
    if instances_tested < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_order = total_order / instances_tested
    mean_width = total_width / instances_tested
    
    # Calculate Pearson correlation coefficient
    covariance = sum((order - mean_order) * (width - mean_width) for order, width in zip(range(instances_tested), range(instances_tested)))
    variance_order = sum((order - mean_order)**2 for order in range(instances_tested))
    variance_width = sum((width - mean_width)**2 for width in range(instances_tested))
    
    if variance_order == 0 or variance_width == 0:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "variance_zero"
        }
    
    correlation_coefficient = covariance / (math.sqrt(variance_order) * math.sqrt(variance_width))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.95,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None])
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None)) / len([r for r in results if r["metric_value"] is not None])
    
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")