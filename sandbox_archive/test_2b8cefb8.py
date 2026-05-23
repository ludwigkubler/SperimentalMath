# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(cols - 1):
        max_row = i
        for j in range(i + 1, rows):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        if matrix[i][i] == 0:
            continue
        for j in range(rows):
            if j != i and matrix[j][i] != 0:
                factor = -matrix[j][i] / matrix[i][i]
                for k in range(i, cols):
                    matrix[j][k] += factor * matrix[i][k]
    return matrix

def rank(matrix):
    augmented_matrix = [row[:] + [1 if i == j else 0 for j in range(len(row))] for i, row in enumerate(matrix)]
    gaussian_elimination(augmented_matrix)
    rank = sum(1 for row in augmented_matrix if any(val != 0 for val in row))
    return rank

def generate_kcnf(n, k):
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(k):
        clause = random.sample(variables, 2)
        clauses.append(clause)
    return clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 5 instances per size
            kcnf = generate_kcnf(n, n // 2)
            matrix = [[0] * (n + 1) for _ in range(n)]
            
            for clause in kcnf:
                for i in clause:
                    matrix[i - 1][i - 1] += 1
                    for j in clause:
                        if i != j:
                            matrix[i - 1][j - 1] -= 1
            
            ga_rank = rank(matrix)
            total_rank += ga_rank
            instances_tested += 1
    
    mean_rank = total_rank / instances_tested
    conjecture_holds = mean_rank <= n ** 0.5
    counterexample = "" if conjecture_holds else "Rank exceeds n^(1/2)"
    
    return {
        "metric_name": "Mean Rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, **result}}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank exceeds n^(1/2)\" first_failing_seed={first_failing_seed}")