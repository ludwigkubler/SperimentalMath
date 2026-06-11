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

def gaussian_elimination(A, b):
    n = len(b)
    A_b = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A_b[j][i]) > abs(A_b[max_row][i]):
                max_row = j
        A_b[i], A_b[max_row] = A_b[max_row], A_b[i]
        for j in range(i+1, n):
            factor = A_b[j][i] / A_b[i][i]
            for k in range(n + 1):
                A_b[j][k] -= factor * A_b[i][k]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (A_b[i][n] - sum(A_b[i][j] * x[j] for j in range(i+1, n))) / A_b[i][i]
    return x

def matrix_multiply(A, B):
    m, k = len(A), len(B[0])
    n = len(B)
    C = [[0] * k for _ in range(m)]
    for i in range(m):
        for j in range(k):
            for l in range(n):
                C[i][j] += A[i][l] * B[l][j]
    return C

def dpll(instance, assignment=None):
    if assignment is None:
        assignment = {}
    n = len(instance)
    unit_clauses = [i for i in range(n) if instance[i].count('1') == 1 or instance[i].count('0') == 1]
    pure_literals = {}
    for clause in instance:
        ones = [int(lit[1:]) for lit in clause.split() if lit.startswith('1')]
        zeros = [int(lit[1:]) for lit in clause.split() if lit.startswith('0')]
        for lit in ones + zeros:
            if lit not in pure_literals:
                pure_literals[lit] = 1
            elif pure_literals[lit] == -1:
                return None
            else:
                pure_literals[lit] += 1
    unit_clauses.extend([lit for lit, count in pure_literals.items() if count > 0])
    unit_clauses.extend([-lit for lit, count in pure_literals.items() if count < 0])
    unit_clauses = list(set(unit_clauses))
    unit_clauses.sort()
    if not unit_clauses:
        return assignment
    lit = unit_clauses[0]
    new_assignment = assignment.copy()
    new_assignment[lit] = True
    result = dpll(instance, new_assignment)
    if result is not None:
        return result
    new_assignment[lit] = False
    result = dpll(instance, new_assignment)
    return result

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    instances_tested = 30
    minInd_values = []
    h_values = []

    for _ in range(instances_tested):
        instance = [''.join(random.choice('10') for _ in range(n)) for _ in range(n)]
        assignment = dpll(instance)
        if assignment is None:
            continue

        # Constructive mapping to compute the clause indicator lattice
        lattice = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if instance[i][j] == '1':
                    lattice[i][j] = 1
                elif instance[i][j] == '0':
                    lattice[i][j] = -1

        # Compute the minimal lattice index (minInd)
        A = [[lattice[i][j] for j in range(n)] for i in range(n)]
        b = [sum(lattice[i]) for i in range(n)]
        x = gaussian_elimination(A, b)
        minInd = sum(abs(val) for val in x)

        # Compute the DPLL search tree height (h)
        h = len(assignment)

        minInd_values.append(minInd)
        h_values.append(h)

    metric_name = "minInd_h_correlation"
    metric_value = sum(minInd * h for minInd, h in zip(minInd_values, h_values)) / sum(h_values)
    n_max = 40
    conjecture_holds = abs(metric_value - (n_max / 2)) <= 3
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")