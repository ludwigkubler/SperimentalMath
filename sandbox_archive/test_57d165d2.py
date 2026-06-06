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
import itertools

def generate_cnf(n, m):
    clauses = []
    for _ in range(m):
        clause = [random.randint(1, n), -random.randint(1, n)]
        clauses.append(clause)
    return clauses

def frobenius_index(cnf):
    if not cnf:
        return 0
    n = len(cnf[0])
    matrix = [[0] * (2 * n) for _ in range(n)]
    for clause in cnf:
        i, j = abs(clause[0]) - 1, abs(clause[1]) - 1
        if clause[0] > 0:
            matrix[i][2 * i] = 1
        else:
            matrix[i][2 * i + 1] = 1
        if clause[1] > 0:
            matrix[j][2 * j] = 1
        else:
            matrix[j][2 * j + 1] = 1
    for i in range(n):
        if matrix[i][i] == 0:
            return float('inf')
    return n

def sat_clause_subset_complexity(cnf):
    max_length = max(len(clause) for clause in cnf)
    return sum(2 ** (len(clause) - 1) for clause in cnf)

def spearman_correlation(x, y):
    if len(x) != len(y):
        raise ValueError("x and y must have the same length")
    n = len(x)
    sorted_x = sorted(range(n), key=lambda i: x[i])
    sorted_y = sorted(range(n), key=lambda i: y[i])
    rank_x = [sorted_x.index(i) for i in range(n)]
    rank_y = [sorted_y.index(i) for i in range(n)]
    d_squared_sum = sum((rank_x[i] - rank_y[i]) ** 2 for i in range(n))
    return 1 - (6 * d_squared_sum) / (n * (n**2 - 1))

def run_trial(seed: int):
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        cnf = generate_cnf(n, 2 * n)
        min_index = frobenius_index(cnf)
        sat_complexity = sat_clause_subset_complexity(cnf)
        if min_index == float('inf'):
            continue
        results.append((min_index, sat_complexity))
    if not results:
        return {
            "metric_name": "Spearman's Rank Correlation Coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "No valid CNF formulas generated"
        }
    x, y = zip(*results)
    correlation = spearman_correlation(x, y)
    return {
        "metric_name": "Spearman's Rank Correlation Coefficient",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation >= 0.8 and all(correlation >= -0.5 for _ in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 100000) for _ in range(30)]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    if all(result is not None for result in results):
        mean = sum(results) / len(results)
        std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
        support_fraction = sum(1 for r in results if r >= 0.8) / len(results)
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(seed for seed, result in zip(seeds, results) if result < 0.8)
            print(f"RESULT: FALSIFIED counterexample='Spearman correlation below threshold' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE some trials produced None")