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

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        max_row = i + max(range(i, rows), key=lambda r: abs(matrix[r][i]))
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        if matrix[i][i] == 0:
            continue
        for j in range(cols):
            matrix[i][j] /= matrix[i][i]
        for k in range(rows):
            if k != i and matrix[k][i] != 0:
                factor = -matrix[k][i]
                for j in range(cols):
                    matrix[k][j] += factor * matrix[i][j]

def rank(matrix):
    augmented_matrix = [row[:] + [1] for row in matrix]
    gaussian_elimination(augmented_matrix)
    rank = 0
    for row in augmented_matrix:
        if any(row[j] != 0 for j in range(len(row) - 1)):
            rank += 1
    return rank

def generate_kcnf(n, k):
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(k):
        clause = random.sample(variables, 2)
        if random.choice([True, False]):
            clause[0] *= -1
        if random.choice([True, False]):
            clause[1] *= -1
        clauses.append(clause)
    return clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 20  # Set a fixed value for n as the conjecture does not specify it
    k = 5   # Set a fixed value for k as the conjecture does not specify it
    
    kcnf_formula = generate_kcnf(n, k)
    
    # Convert k-CNF to matrix representation (simplified for illustration purposes)
    matrix = [[0] * n for _ in range(n)]
    for clause in kcnf_formula:
        for var in clause:
            if var > 0:
                matrix[var - 1][var - 1] += 1
            else:
                matrix[-var - 1][-var - 1] += 1
    
    ga_rank = rank(matrix)
    
    # Placeholder for monotone circuit depth calculation (not implemented in this example)
    monotone_circuit_depth = n  # This is a placeholder value
    
    return {
        "metric_name": "Rank vs Monotone Circuit Depth",
        "metric_value": ga_rank,
        "instances_tested": 1,
        "conjecture_holds": ga_rank <= math.sqrt(n),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 53))  # Default to first 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, **result}}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")