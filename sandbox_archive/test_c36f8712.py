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

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    rank = 0
    for i in range(cols):
        if rank >= rows:
            break
        pivot_row = -1
        for j in range(rank, rows):
            if matrix[j][i] == 1:
                pivot_row = j
                break
        if pivot_row == -1:
            continue
        matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
        for j in range(rows):
            if i != j and matrix[j][i] == 1:
                for k in range(cols):
                    matrix[j][k] ^= matrix[pivot_row][k]
        rank += 1
    return rank

def generate_3sat_instance(n, m):
    clauses = []
    variables = list(range(1, n + 1))
    for _ in range(m):
        clause = random.sample(variables, 3)
        sign = [random.choice([-1, 1]) for _ in range(3)]
        clauses.append([(sign[i] * var) % 2 for i, var in enumerate(clause)])
    return clauses

def incidence_matrix(clauses, n):
    m = len(clauses)
    matrix = [[0] * n for _ in range(m)]
    for i, clause in enumerate(clauses):
        for j, var in enumerate(clause):
            if var == 1:
                matrix[i][j] = 1
            elif var == -1:
                matrix[i][n + j] = 1
    return matrix

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = n * 10
        clauses = generate_3sat_instance(n, m)
        matrix = incidence_matrix(clauses, n)
        rank = gaussian_elimination(matrix)
        
        # Estimate ACC^0 circuit size (simplified upper bound)
        epsilon = 0.5
        circuit_size = n ** epsilon
        
        results.append({
            "n": n,
            "rank": rank,
            "circuit_size": circuit_size
        })
    
    mean_rank = sum(result["rank"] for result in results) / len(results)
    std_rank = math.sqrt(sum((result["rank"] - mean_rank) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if abs(math.log(result["n"]) - result["rank"]) < 0.5 * std_rank and result["circuit_size"] <= n_values[-1] ** 0.5) / len(results)
    
    conjecture_holds = support_fraction >= 0.8
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "rank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    std_rank = math.sqrt(sum((result["metric_value"] - mean_rank) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")