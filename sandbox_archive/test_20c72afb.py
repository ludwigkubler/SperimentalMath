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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        pivot = A[i][i]
        for j in range(n):
            A[i][j] /= pivot
        for j in range(n):
            if j != i:
                factor = A[j][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]

def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def quadratic_form(literals, clauses):
    n = len(literals)
    Q = [[0] * n for _ in range(n)]
    for clause in clauses:
        i, j = [int(lit[2:]) - 1 for lit in clause if not lit.startswith('~')]
        Q[i][j] += 1
        Q[j][i] += 1
    gaussian_elimination(Q)
    min_rank = sum(1 for row in Q if any(row))
    return min_rank

def resolution_width(clauses):
    n = len(clauses)
    width = [0] * n
    for i in range(n):
        for j in range(i+1, n):
            if not set(clauses[i]).isdisjoint(set(clauses[j])):
                width[i] += 1
                width[j] += 1
    return max(width)

def Tseitin_formula(n):
    literals = [f'x{i}' for i in range(1, n+1)]
    clauses = []
    for i in range(1, n+1):
        clauses.append([f'~{literals[i-1]}', f'|{literals[i-1]}'])
    return literals, clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        literals, clauses = Tseitin_formula(n)
        min_rank = quadratic_form(literals, clauses)
        w = resolution_width(clauses)
        results.append((min_rank, w))
    if len(results) < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for _, n in results),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    min_ranks = [r[0] for r in results]
    widths = [r[1] for r in results]
    mean_min_rank = sum(min_ranks) / len(min_ranks)
    mean_width = sum(widths) / len(widths)
    correlation_coefficient = sum((min_ranks[i] - mean_min_rank) * (widths[i] - mean_width) for i in range(len(results))) / len(results)
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": 30,
        "n_max": max(n for _, n in results),
        "conjecture_holds": abs(correlation_coefficient) > 0.9 and mean_min_rank - mean_width < 2 and mean_width - mean_min_rank < 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [random.getrandbits(32) for _ in range(30)]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"n_max\": {trial_result['n_max']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")
        results.append(trial_result)
    mean_metric_value = sum(r['metric_value'] for r in results if r['metric_value'] is not None) / len([r for r in results if r['metric_value'] is not None])
    std_metric_value = math.sqrt(sum((r['metric_value'] - mean_metric_value)**2 for r in results if r['metric_value'] is not None) / len([r for r in results if r['metric_value'] is not None]))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results):
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")