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
    
    n = 20  # Number of variables
    m = 10  # Number of clauses
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n) if random.choice([True, False]) else -random.randint(1, n) for _ in range(random.randint(1, n))]
            cnf.append(clause)
        return cnf
    
    def gram_matrix(cnf):
        G = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in cnf:
            for lit in clause:
                if lit > 0:
                    i = lit
                else:
                    i = -lit
                G[i][i] += 1
        return G
    
    def matrix_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for col in range(n):
            if all(matrix[row][col] == 0 for row in range(m)):
                continue
            pivot_row = next(row for row in range(col, m) if matrix[row][col] != 0)
            matrix[col], matrix[pivot_row] = matrix[pivot_row], matrix[col]
            rank += 1
            for row in range(m):
                if row == col:
                    continue
                factor = -matrix[row][col] / matrix[col][col]
                for j in range(n + 1):
                    matrix[row][j] += factor * matrix[col][j]
        return rank
    
    cnf = generate_cnf(n, m)
    G_F = gram_matrix(cnf)
    rank_G_F = matrix_rank(G_F)
    
    metric_value = rank_G_F
    conjecture_holds = 0 <= metric_value <= 10 * n**2 / m
    counterexample = "" if conjecture_holds else f"Rank {metric_value} exceeds bound 10n^2/m"
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank exceeds bound\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")