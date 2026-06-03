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
    
    def generate_communication_matrix(n):
        matrix = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        return matrix
    
    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        augmented_matrix = [row + [1 if i == j else 0 for j in range(m)] for i, row in enumerate(matrix)]
        pivot_row = 0
        for col in range(n):
            if all(augmented_matrix[row][col] == 0 for row in range(pivot_row, m)):
                continue
            augmented_matrix[pivot_row], augmented_matrix[col + pivot_row] = augmented_matrix[col + pivot_row], augmented_matrix[pivot_row]
            for row in range(m):
                if row != pivot_row and augmented_matrix[row][col] != 0:
                    factor = -augmented_matrix[row][col] / augmented_matrix[pivot_row][col]
                    augmented_matrix[row] = [a + b * factor for a, b in zip(augmented_matrix[row], augmented_matrix[pivot_row])]
            pivot_row += 1
        return pivot_row
    
    def minimal_rank(quasi_group_extension):
        # Placeholder implementation of minimal rank calculation
        return len(quasi_group_extension)
    
    n_values = [5, 10, 15, 20, 30, 40]
    communication_matrix_ranks = []
    minimal_ranks = []
    
    for n in n_values:
        matrix = generate_communication_matrix(n)
        comm_rank = rank(matrix)
        quasi_group_extension = matrix  # Placeholder for actual quasi-group extension
        min_rank = minimal_rank(quasi_group_extension)
        
        communication_matrix_ranks.append(comm_rank)
        minimal_ranks.append(min_rank)
    
    correlation_coefficient = sum((x - mean_x) * (y - mean_y) for x, y in zip(communication_matrix_ranks, minimal_ranks)) / \
                              math.sqrt(sum((x - mean_x) ** 2 for x in communication_matrix_ranks) *
                                        sum((y - mean_y) ** 2 for y in minimal_ranks))
    
    mean_comm_rank = sum(communication_matrix_ranks) / len(communication_matrix_ranks)
    mean_min_rank = sum(minimal_ranks) / len(minimal_ranks)
    
    within_10_percent_comm = all(abs(x - mean_comm_rank) <= 0.1 * abs(mean_comm_rank) for x in communication_matrix_ranks)
    within_10_percent_min = all(abs(x - mean_min_rank) <= 0.1 * abs(mean_min_rank) for x in minimal_ranks)
    
    conjecture_holds = correlation_coefficient >= 0.9 and within_10_percent_comm and within_10_percent_min
    counterexample = 'not_within_10_percent' if not within_10_percent_comm or not within_10_percent_min else ''
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='{result['counterexample']}' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")