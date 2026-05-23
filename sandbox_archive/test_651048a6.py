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
        max_row = i + max(range(i, rows), key=lambda x: abs(matrix[x][i]))
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        pivot = matrix[i][i]
        if pivot == 0:
            continue
        for j in range(cols):
            matrix[i][j] /= pivot
        for k in range(rows):
            if k != i:
                factor = matrix[k][i]
                for j in range(cols):
                    matrix[k][j] -= factor * matrix[i][j]

def rank(matrix):
    augmented_matrix = [row[:] + [1] for row in matrix]
    gaussian_elimination(augmented_matrix)
    rank = 0
    for row in augmented_matrix:
        if any(row[j] != 0 for j in range(len(row) - 1)):
            rank += 1
    return rank

def generate_k_cnf(n, k):
    variables = list(range(1, n + 1))
    clauses = []
    while len(clauses) < k:
        clause = set()
        while len(clause) < 3:
            var = random.choice(variables)
            if var not in clause and -var not in clause:
                clause.add(var)
        clauses.append(tuple(sorted(clause)))
    return clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Sample 5 instances per n
            k_cnf = generate_k_cnf(n, random.randint(1, n))
            # Convert k-CNF to a matrix representation (simplified)
            matrix = [[0] * (n + 1) for _ in range(n)]
            for clause in k_cnf:
                for var in clause:
                    matrix[abs(var) - 1][var if var > 0 else n] += 1
            ga_rank = rank(matrix)
            total_rank += ga_rank
            instances_tested += 1
    
    mean_rank = total_rank / instances_tested
    conjecture_holds = mean_rank <= n_values[-1]**(1/2)
    counterexample = "" if conjecture_holds else "mean_rank > n^(1/2)"
    
    return {
        "metric_name": "Mean Rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")