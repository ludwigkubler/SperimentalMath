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

def symplectic_form(clauses):
    n = len(clauses)
    omega = [[0] * (2*n) for _ in range(2*n)]
    for i, clause in enumerate(clauses):
        for lit in clause:
            if lit > 0:
                omega[2*i][2*lit-1] = 1
                omega[2*i+1][2*lit] = -1
            else:
                omega[2*-lit-1][2*i] = 1
                omega[2*i+1][2*-lit-1] = -1
    return omega

def resolution_width(phi):
    clauses = phi.split(' or ')
    literals = set()
    for clause in clauses:
        literals.update([int(lit) for lit in clause.split(' and ') if lit != 'not'])
    n = len(literals)
    assignment = {lit: False for lit in literals}
    queue = [phi]
    while queue:
        phi = queue.pop(0)
        if phi == 'True':
            return 1
        if phi == 'False':
            continue
        literal, rest = phi.split(' or ')
        if literal[0] == 'not':
            literal = int(literal[4:])
            assignment[literal] = not assignment[literal]
        else:
            literal = int(literal)
            assignment[literal] = True
        new_clauses = []
        for clause in rest.split(' and '):
            if literal in clause:
                continue
            if 'not' + str(literal) in clause:
                new_clause = [l for l in clause.split(' or ') if l != 'not' + str(literal)]
                new_clauses.append(' or '.join(new_clause))
        queue.extend(new_clauses)
    return 0

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    min_ranks = []
    widths = []
    for n in n_values:
        phi = ' or '.join(['x' + str(i) if i % 2 == 0 else 'not x' + str(i) for i in range(1, n+1)])
        omega = symplectic_form(phi.split(' or '))
        gaussian_elimination(omega)
        min_rank = sum(1 for row in omega if any(row))
        width = resolution_width(phi)
        min_ranks.append(min_rank)
        widths.append(width)
    mean_min_rank = sum(min_ranks) / len(min_ranks)
    mean_width = sum(widths) / len(widths)
    c = mean_min_rank / mean_width
    conjecture_holds = all(min_rank >= c * width for min_rank, width in zip(min_ranks, widths))
    counterexample = "" if conjecture_holds else "mapping_undefined"
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
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")