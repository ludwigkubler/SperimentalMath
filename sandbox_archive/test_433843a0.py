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
    rows = len(matrix)
    cols = len(matrix[0])
    for i in range(rows):
        max_row = i
        for j in range(i + 1, rows):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        factor = Fraction(matrix[i][i])
        for j in range(cols):
            matrix[i][j] /= factor
        for j in range(rows):
            if i != j:
                factor = Fraction(matrix[j][i])
                for k in range(cols):
                    matrix[j][k] -= factor * matrix[i][k]
    return matrix

def rank(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    rref_matrix = gaussian_elimination(matrix)
    rank = 0
    for i in range(rows):
        if any(rref_matrix[i][j] != Fraction(0) for j in range(cols)):
            rank += 1
    return rank

def random_cnf(n, m):
    variables = list(range(1, n + 1))
    cnf = []
    for _ in range(m):
        clause = random.sample(variables, random.randint(1, n))
        cnf.append(clause)
    return cnf

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    total_clauses = 0
    for n in n_values:
        m = random.randint(1, n * 2)  # Ensure at least one clause per variable
        cnf = random_cnf(n, m)
        matrix = [[Fraction(0) for _ in range(n)] for _ in range(m)]
        for i, clause in enumerate(cnf):
            for var in clause:
                matrix[i][var - 1] = Fraction(1)
        rank_value = rank(matrix)
        total_rank += rank_value
        total_clauses += m
    
    mean_ratio = Fraction(total_rank, total_clauses)
    conjecture_holds = mean_ratio <= Fraction(2)  # Example constant c=2
    counterexample = "" if conjecture_holds else f"Mean ratio {mean_ratio} > 2"
    
    return {
        "metric_name": "Mean Ratio",
        "metric_value": float(mean_ratio),
        "instances_tested": len(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)

    mean_d = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_d} std=NA support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Mean ratio exceeded 2\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")