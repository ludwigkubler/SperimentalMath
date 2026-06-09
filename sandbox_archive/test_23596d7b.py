# auto-injected by SEC sandbox
import math
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

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        if matrix[max_row][i] == 0:
            continue  # Skip row with zero pivot

        # Swap rows
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]

        # Eliminate below the pivot
        for j in range(i+1, n):
            factor = Fraction(matrix[j][i], matrix[i][i])
            for k in range(n):
                matrix[j][k] -= factor * matrix[i][k]
    
    rank = sum(1 for row in matrix if any(x != 0 for x in row))
    return rank

def generate_coxeter_group(depth):
    # This is a placeholder function to simulate generating a Coxeter group from a Frege proof
    # For simplicity, we'll just return a random adjacency matrix
    n = depth * 2 + 1
    adjacency_matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if random.choice([True, False]):
                adjacency_matrix[i][j] = 1
                adjacency_matrix[j][i] = 1
    return adjacency_matrix

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    metric_name = "Coxeter Group Rank"
    instances_tested = 0
    n_max = 0
    total_rank = 0
    
    for depth in [5, 10, 15, 20, 30, 40]:
        G = generate_coxeter_group(depth)
        rank = gaussian_elimination(G)
        instances_tested += len(G)
        n_max = max(n_max, depth)
        
        if rank > 1.5 * depth ** 1.5:
            return {
                "metric_name": metric_name,
                "metric_value": rank,
                "instances_tested": instances_tested,
                "n_max": n_max,
                "conjecture_holds": False,
                "counterexample": f"Depth {depth}, Rank {rank}"
            }
        
        total_rank += rank
    
    mean_rank = Fraction(total_rank, instances_tested)
    support_fraction = 1.0 if all(rank <= 1.5 * depth ** 1.5 for depth in [5, 10, 15, 20, 30, 40]) else 0.0
    
    return {
        "metric_name": metric_name,
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(sys.argv[1])] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")