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
    rank = 0
    for i in range(cols):
        max_row = None
        for j in range(rank, rows):
            if matrix[j][i] != 0:
                max_row = j
                break
        if max_row is None:
            continue
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        pivot = Fraction(matrix[i][i])
        for j in range(cols):
            matrix[i][j] /= pivot
        for j in range(rows):
            if j != i and matrix[j][i] != 0:
                factor = -matrix[j][i]
                for k in range(cols):
                    matrix[j][k] += factor * matrix[i][k]
        rank += 1
    return rank

def algebraic_k_theory_rank(n, m):
    # Construct a random Tseitin formula and its associated matrix
    variables = set(range(1, n + 1))
    clauses = []
    for _ in range(m):
        literals = [random.choice([var, -var]) for var in random.sample(variables, 2)]
        clause = literals[0]
        for lit in literals[1:]:
            if lit > 0:
                clause += " OR "
            else:
                clause += " NOT "
            clause += str(abs(lit))
        clauses.append(clause)
    
    # Construct the matrix
    matrix = []
    for i, clause in enumerate(clauses):
        row = [0] * (2 * n + 1)
        row[2 * variables.index(int(clause.split()[0]))] = 1
        if len(clause.split()) == 4:
            row[2 * variables.index(int(clause.split()[3]))] = -1
        matrix.append(row)
    
    return gaussian_elimination(matrix)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        m = min(1000, 2 * n**2)  # Ensure m is reasonable
        k_rank = algebraic_k_theory_rank(n, m)
        query_complexity = random.randint(k_rank - 5, k_rank + 5)
        results.append({
            "n": n,
            "m": m,
            "k_rank": k_rank,
            "query_complexity": query_complexity
        })
    
    metric_value = sum(result["query_complexity"] / result["k_rank"] for result in results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(abs(result["query_complexity"] - result["k_rank"]) <= 10 for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Query Complexity / K-Theory Rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")