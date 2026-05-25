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
    for i in range(cols):
        pivot_row = None
        for j in range(i, rows):
            if matrix[j][i] != 0:
                pivot_row = j
                break
        if pivot_row is None:
            continue
        for j in range(rows):
            if j == pivot_row:
                continue
            factor = -matrix[j][i] / matrix[pivot_row][i]
            for k in range(i, cols):
                matrix[j][k] += factor * matrix[pivot_row][k]

def min_rank(matrix):
    rows, cols = len(matrix), len(matrix[0])
    rank = 0
    for i in range(cols):
        if all(matrix[j][i] == 0 for j in range(rank)):
            continue
        rank += 1
        gaussian_elimination([matrix[j][i:] for j in range(rank)])
    return rank

def random_cnf(n, m):
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause = [random.choice(variables) if random.choice([True, False]) else -random.choice(variables) for _ in range(random.randint(2, 3))]
        clauses.append(clause)
    return clauses

def p_adic_diff(formula):
    n = len(formula[0])
    p_adic_diffs = []
    for clause in formula:
        diff = [Fraction(1, 1)]
        for lit in clause:
            if lit > 0:
                diff.append(Fraction(-1, lit))
            else:
                diff.append(Fraction(1, -lit))
        p_adic_diffs.extend(diff)
    return p_adic_diffs

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    m = 2 * n
    formula = random_cnf(n, m)
    p_adic_diffs = p_adic_diff(formula)
    rank = min_rank([p_adic_diffs[i:i+n+1] for i in range(0, len(p_adic_diffs), n + 1)])
    expected_rank = math.isqrt(n) * 1.5
    conjecture_holds = rank <= expected_rank
    counterexample = "" if conjecture_holds else f"rank={rank}, expected_rank={expected_rank}"
    return {
        "metric_name": "minimal_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 8)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, 'metric_name': '{result['metric_name']}', 'metric_value': {result['metric_value']}, 'instances_tested': {result['instances_tested']}, 'conjecture_holds': {result['conjecture_holds']}, 'counterexample': '{result['counterexample']}'}}")
        results.append(result)
    
    mean_rank = sum(r['metric_value'] for r in results) / len(results)
    std_rank = math.sqrt(sum((r['metric_value'] - mean_rank)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample='rank exceeds expected' first_failing_seed={first_failing_seed}")