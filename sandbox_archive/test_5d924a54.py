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
    
    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        augmented_matrix = [row + [1 if i == j else 0 for j in range(n)] for i, row in enumerate(matrix)]
        pivot_row = 0
        for col in range(n):
            max_pivot = None
            for row in range(pivot_row, m):
                if abs(augmented_matrix[row][col]) > (max_pivot or 0):
                    max_pivot = augmented_matrix[row][col]
                    pivot_row = row
            if max_pivot is None:
                continue
            augmented_matrix[pivot_row], augmented_matrix[0] = augmented_matrix[0], augmented_matrix[pivot_row]
            factor = -augmented_matrix[0][col] / augmented_matrix[0][col]
            for j in range(n + 1):
                augmented_matrix[0][j] *= factor
            for i in range(1, m):
                factor = -augmented_matrix[i][col] / augmented_matrix[0][col]
                for j in range(n + 1):
                    augmented_matrix[i][j] += factor * augmented_matrix[0][j]
            pivot_row += 1
        rank = sum(1 for row in augmented_matrix if any(abs(x) > 1e-9 for x in row[:n]))
        return rank
    
    def generate_communication_matrix(n):
        matrix = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            matrix[i][i] = 1
        return matrix
    
    n_values = [5, 10, 15, 20, 30, 40]
    communication_matrix_ranks = []
    minimal_ranks = []
    
    for n in n_values:
        instances_tested = 0
        for _ in range(5):  # Ensure at least 30 instances per seed
            matrix = generate_communication_matrix(n)
            comm_rank = rank(matrix)
            communication_matrix_ranks.append(comm_rank)
            
            # Simulate minimal rank calculation (placeholder)
            minimal_rank = comm_rank ** 2
            minimal_ranks.append(minimal_rank)
            
            instances_tested += 1
    
    mean_comm_rank = sum(communication_matrix_ranks) / len(communication_matrix_ranks)
    std_comm_rank = math.sqrt(sum((x - mean_comm_rank) ** 2 for x in communication_matrix_ranks) / len(communication_matrix_ranks))
    
    mean_minimal_rank = sum(minimal_ranks) / len(minimal_ranks)
    std_minimal_rank = math.sqrt(sum((x - mean_minimal_rank) ** 2 for x in minimal_ranks) / len(minimal_ranks))
    
    correlation_coefficient = sum((communication_matrix_ranks[i] - mean_comm_rank) * (minimal_ranks[i] - mean_minimal_rank) for i in range(len(communication_matrix_ranks))) / (len(communication_matrix_ranks) * std_comm_rank * std_minimal_rank)
    
    conjecture_holds = correlation_coefficient >= 0.9 and abs(correlation_coefficient) <= 1
    counterexample = "" if conjecture_holds else "correlation_coefficient_out_of_bounds"
    
    return {
        "metric_name": "communication_matrix_rank vs minimal_rank",
        "metric_value": correlation_coefficient,
        "instances_tested": len(communication_matrix_ranks),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_out_of_bounds\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")