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
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i
        for j in range(i + 1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        pivot = A[i][i]
        if pivot == 0:
            continue
        for j in range(n):
            A[i][j] /= pivot
        for j in range(m):
            if j != i and A[j][i] != 0:
                factor = A[j][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]

def matrix_multiply(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def symplectic_form(clauses):
    n = len(clauses)
    omega = [[0] * (2 * n) for _ in range(2 * n)]
    for i, clause in enumerate(clauses):
        for lit in clause.split(' or '):
            if lit.startswith('-'):
                j = int(lit[1:]) - 1
                omega[i][n + j] = 1
                omega[n + j][i] = 1
            else:
                j = int(lit) - 1
                omega[j][j] = 1
    gaussian_elimination(omega)
    min_rank = sum(row.count(0) for row in omega if any(x != 0 for x in row))
    return min_rank

def resolution_width(phi):
    clauses = phi.split(' and ')
    stack = []
    while clauses:
        clause = clauses.pop()
        if ' or ' not in clause:
            continue
        literals = clause.split(' or ')
        pos_lit = next((lit for lit in literals if not lit.startswith('-')), None)
        neg_lit = next((lit for lit in literals if lit.startswith('-')), None)
        if pos_lit and neg_lit:
            stack.append(neg_lit[1:])
            clauses.extend([c.replace(pos_lit, '').replace(' or ' + pos_lit, '') for c in clauses])
            clauses.extend([c.replace(neg_lit, '').replace(' or ' + neg_lit, '') for c in clauses])
        else:
            return len(stack)
    return 0

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    min_ranks = []
    widths = []
    for n in n_values:
        phi = ' and '.join(' or '.join(str(random.randint(1, n)) for _ in range(n)) for _ in range(n))
        min_rank = symplectic_form(phi)
        width = resolution_width(phi)
        min_ranks.append(min_rank)
        widths.append(width)
    mean_min_rank = sum(min_ranks) / len(min_ranks)
    mean_width = sum(widths) / len(widths)
    c = Fraction(mean_min_rank, mean_width)
    conjecture_holds = all(min_rank >= c * width for min_rank, width in zip(min_ranks, widths))
    counterexample = "" if conjecture_holds else "c_value_too_small"
    return {
        "metric_name": "min_rank_over_width",
        "metric_value": mean_min_rank / mean_width,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"c_value_too_small\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")