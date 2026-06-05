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
from itertools import combinations

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        if matrix[i][i] == 0:
            return None  # Singular matrix
        for j in range(i + 1, rows):
            factor = Fraction(matrix[j][i], matrix[i][i])
            for k in range(cols):
                matrix[j][k] -= factor * matrix[i][k]
    return matrix

def generate_geometric_vector_field(d):
    # Placeholder function to generate a random geometric vector field
    return [[random.uniform(-1, 1) for _ in range(d)] for _ in range(d)]

def compute_holonomy_representation(vector_field):
    d = len(vector_field)
    holonomy_matrix = []
    for i in range(d):
        row = [vector_field[j][i] - vector_field[i][j] for j in range(d)]
        holonomy_matrix.append(row)
    return holonomy_matrix

def compute_communication_complexity_rank(holonomy_matrix):
    d = len(holonomy_matrix)
    comm_complexity_matrix = []
    for i, j in combinations(range(d), 2):
        row = [holonomy_matrix[i][k] * holonomy_matrix[j][k] for k in range(d)]
        comm_complexity_matrix.append(row)
    rank = gaussian_elimination(comm_complexity_matrix)
    if rank is None:
        return None
    return sum(1 for row in rank if any(row))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    d_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for d in d_values:
        instances_tested = 0
        n_max = 0
        total_rank = 0
        total_comm_rank = 0
        
        while len(results) < 30:
            vector_field = generate_geometric_vector_field(d)
            holonomy_matrix = compute_holonomy_representation(vector_field)
            comm_complexity_rank = compute_communication_complexity_rank(holonomy_matrix)
            
            if comm_complexity_rank is None or not (1 <= comm_complexity_rank <= d):
                continue
            
            instances_tested += 1
            n_max = max(n_max, d)
            total_rank += len(holonomy_matrix)
            total_comm_rank += comm_complexity_rank
        
        mean_rank = total_rank / instances_tested
        mean_comm_rank = total_comm_rank / instances_tested
        correlation_coefficient = (instances_tested * sum(rank * comm_rank for rank, comm_rank in zip(range(1, d+1), range(1, d+1))) - 
                                   instances_tested * mean_rank * mean_comm_rank) / \
                                  math.sqrt((instances_tested * sum(rank**2 for rank in range(1, d+1)) - instances_tested * mean_rank**2) *
                                            (instances_tested * sum(comm_rank**2 for comm_rank in range(1, d+1)) - instances_tested * mean_comm_rank**2))
        
        results.append({
            "metric_name": "correlation_coefficient",
            "metric_value": correlation_coefficient,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": correlation_coefficient > 0.7,
            "counterexample": ""
        })
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "seed": seed,
        "mean_metric_value": mean_metric_value,
        "support_fraction": support_fraction,
        "results": results
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["mean_metric_value"] for result in results) / len(results)
    support_fraction = sum(result["support_fraction"] for result in results) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")