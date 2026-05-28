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
        max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
        A[i], A[max_row] = A[max_row], A[i]
        if A[i][i] == 0:
            continue
        denom = A[i][i]
        for j in range(n):
            A[i][j] /= denom
        for k in range(n):
            if k != i and A[k][i] != 0:
                factor = A[k][i]
                for j in range(n):
                    A[k][j] -= factor * A[i][j]
    return A

def matrix_rank(A):
    n = len(A)
    rank = 0
    for i in range(n):
        if all(abs(A[j][i]) < 1e-9 for j in range(rank)):
            continue
        rank += 1
        denom = A[i][i]
        for j in range(n):
            A[i][j] /= denom
        for k in range(n):
            if k != i and abs(A[k][i]) > 1e-9:
                factor = A[k][i]
                for j in range(n):
                    A[k][j] -= factor * A[i][j]
    return rank

def convert_matrix_to_cnf(A):
    n = len(A)
    cnf = []
    for i in range(n):
        for j in range(i + 1, n):
            if A[i][j] != 0:
                clause = [i * n + j + 1, -(i * n + i + 1), -(j * n + j + 1)]
                cnf.append(clause)
    return cnf

def dpll_search_tree_height(cnf):
    def dpll(assignment):
        if not cnf:
            return 0
        unit_clauses = [c for c in cnf if len(c) == 1]
        if unit_clauses:
            literal = unit_clauses[0][0]
            new_assignment = assignment[:]
            new_assignment[abs(literal) - 1] = literal > 0
            return dpll(new_assignment)
        pure_literals = [l for l in range(1, n * n + 1) if (all(l not in c for c in cnf) or all(-l not in c for c in cnf))]
        if pure_literals:
            literal = pure_literals[0]
            new_assignment = assignment[:]
            new_assignment[abs(literal) - 1] = literal > 0
            return dpll(new_assignment)
        literal = random.choice([l for l in range(1, n * n + 1)])
        new_assignment_true = assignment[:]
        new_assignment_true[abs(literal) - 1] = literal > 0
        height_true = dpll(new_assignment_true)
        if height_true == float('inf'):
            return float('inf')
        new_assignment_false = assignment[:]
        new_assignment_false[abs(literal) - 1] = literal < 0
        height_false = dpll(new_assignment_false)
        if height_false == float('inf'):
            return float('inf')
        return max(height_true, height_false) + 1
    n = int(math.sqrt(len(cnf)))
    assignment = [False] * (n * n)
    return dpll(assignment)

def symplectic_leaves_rank(A):
    # Placeholder for the actual implementation of symplectic leaves rank calculation
    return matrix_rank(gaussian_elimination(A))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    A = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            A[j][i] = A[i][j]
    cnf = convert_matrix_to_cnf(A)
    h_A = dpll_search_tree_height(cnf)
    kappa_L_A = symplectic_leaves_rank(A)
    if h_A == float('inf'):
        return {
            "metric_name": "kappa_L_A / c * h_A",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "DPLL search tree height is infinite"
        }
    if kappa_L_A > 1000:  # Arbitrary large number to avoid trivial cases
        return {
            "metric_name": "kappa_L_A / c * h_A",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Symplectic leaves rank is too large"
        }
    if kappa_L_A <= 0:
        return {
            "metric_name": "kappa_L_A / c * h_A",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Symplectic leaves rank is non-positive"
        }
    c = Fraction(1, 2)  # Placeholder for the actual constant
    return {
        "metric_name": "kappa_L_A / c * h_A",
        "metric_value": kappa_L_A / (c * h_A),
        "instances_tested": 1,
        "conjecture_holds": kappa_L_A <= c * h_A,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        results.append(trial_result)
        print(f"TRIAL: {trial_result}")
    
    if all(result["conjecture_holds"] for result in results):
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"kappa_L_A > c * h_A\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")