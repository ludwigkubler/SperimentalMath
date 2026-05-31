# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations, product

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        max_row = i + max(range(i, rows), key=lambda r: abs(matrix[r][i]))
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        for j in range(cols):
            if i != j:
                factor = Fraction(matrix[j][i], matrix[i][i])
                for k in range(i, cols):
                    matrix[j][k] -= factor * matrix[i][k]
    return matrix

def matrix_multiplication(A, B):
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])
    result = [[Fraction(0) for _ in range(cols_B)] for _ in range(rows_A)]
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]
    return result

def dpll(instance, assignment=None):
    if assignment is None:
        assignment = [-1] * len(instance)
    
    def find_unassigned():
        for i in range(len(assignment)):
            if assignment[i] == -1:
                return i
        return None
    
    unassigned = find_unassigned()
    if unassigned is None:
        return True, sum(abs(x) for x in assignment)
    
    literal = 2 * unassigned + (1 if random.choice([True, False]) else 0)
    new_assignment = assignment[:]
    new_assignment[unassigned] = literal % 2
    
    result, path_length = dpll(instance, new_assignment)
    if result:
        return True, path_length
    
    new_assignment[unassigned] = (literal + 1) % 2
    result, path_length = dpll(instance, new_assignment)
    return result, path_length

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_instance(n):
        clauses = []
        for _ in range(2 ** n):
            clause = [random.choice([-1, 1]) * i for i in range(n)]
            if all(x == 0 for x in clause):
                continue
            clauses.append(clause)
        return clauses
    
    def quandle_action_group(instance):
        # Placeholder for actual quandle action group computation
        return set()
    
    n_values = [5, 10, 15, 20, 30, 40]
    metrics = []
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):
            instance = generate_instance(n)
            assignment = [-1] * len(instance)
            
            path_length = dpll(instance, assignment)[1]
            m_index = len(quandle_action_group(instance))
            
            metrics.append({"m_index": m_index, "path_length": path_length})
            instances_tested += 1
            n_max = max(n_max, n)
    
    if not metrics:
        return {
            "metric_name": "m_index",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    m_indices = [m["m_index"] for m in metrics]
    path_lengths = [m["path_length"] for m in metrics]
    
    mean_m_index = sum(m_indices) / len(m_indices)
    mean_path_length = sum(path_lengths) / len(path_lengths)
    
    correlation_coefficient = 0
    if len(metrics) > 1:
        numerator = sum((x - mean_m_index) * (y - mean_path_length) for x, y in zip(m_indices, path_lengths))
        denominator = math.sqrt(sum((x - mean_m_index) ** 2 for x in m_indices)) * math.sqrt(sum((y - mean_path_length) ** 2 for y in path_lengths))
        correlation_coefficient = numerator / denominator
    
    conjecture_holds = correlation_coefficient >= 0.8 and max(m_indices) <= 10
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.8 or m_index > 10"
    
    return {
        "metric_name": "m_index",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")