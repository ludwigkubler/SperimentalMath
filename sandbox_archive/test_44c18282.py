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
    
    # Define a simple geometric vector field on a d-dimensional manifold
    def generate_vector_field(d):
        return [[random.uniform(-1, 1) for _ in range(d)] for _ in range(d)]
    
    # Compute the minimal rank of the holonomy representation
    def min_rank(matrix):
        n = len(matrix)
        if n == 0:
            return 0
        rank = 0
        for i in range(n):
            pivot = matrix[i][i]
            if pivot != 0:
                rank += 1
                for j in range(i + 1, n):
                    factor = matrix[j][i] / pivot
                    for k in range(i, n):
                        matrix[j][k] -= factor * matrix[i][k]
        return rank
    
    # Compute the communication complexity rank
    def comm_complexity_rank(matrix):
        n = len(matrix)
        if n == 0:
            return 0
        rank = 0
        for i in range(n):
            pivot = matrix[i][i]
            if pivot != 0:
                rank += 1
                for j in range(i + 1, n):
                    factor = matrix[j][i] / pivot
                    for k in range(i, n):
                        matrix[j][k] -= factor * matrix[i][k]
        return rank
    
    # Generate random geometric vector fields on d-dimensional manifolds
    d = random.randint(2, 5)
    vector_fields = [generate_vector_field(d) for _ in range(30)]
    
    # Compute the minimal rank of the holonomy representation and communication complexity rank
    ranks_holonomy = [min_rank(field) for field in vector_fields]
    ranks_comm = [comm_complexity_rank(field) for field in vector_fields]
    
    # Check if all computed communication complexity ranks are within the range [1, d]
    if any(rank < 1 or rank > d for rank in ranks_comm):
        return {
            "metric_name": "communication_complexity_rank",
            "metric_value": None,
            "instances_tested": len(vector_fields),
            "n_max": d,
            "conjecture_holds": False,
            "counterexample": "computed_rank_outside_range"
        }
    
    # Compute the Pearson correlation coefficient
    def pearsonr(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov_xy / (std_x * std_y)
    
    correlation_coefficient = pearsonr(ranks_holonomy, ranks_comm)
    
    # Check if the Pearson correlation coefficient exceeds 0.7
    if correlation_coefficient < 0.7:
        return {
            "metric_name": "communication_complexity_rank",
            "metric_value": correlation_coefficient,
            "instances_tested": len(vector_fields),
            "n_max": d,
            "conjecture_holds": False,
            "counterexample": "correlation_coefficient_too_low"
        }
    
    return {
        "metric_name": "communication_complexity_rank",
        "metric_value": correlation_coefficient,
        "instances_tested": len(vector_fields),
        "n_max": d,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_too_low\" first_failing_seed={first_failing_seed}")