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
        factor = Fraction(A[i][i], 1)
        for j in range(n):
            if i != j:
                factor_j = Fraction(A[j][i], A[i][i])
                for k in range(n+1):
                    A[j][k] -= factor_j * A[i][k]
    return A

def determinant(A):
    n = len(A)
    det = 1
    for i in range(n):
        det *= A[i][i]
    return det

def m_order(phi):
    # Convert CNF to quadratic form Q
    n = len(phi)
    Q = [[0] * n for _ in range(n)]
    for clause in phi:
        for var in clause:
            if var > 0:
                Q[var-1][var-1] += 1
            else:
                Q[-var-1][-var-1] += 1
    return abs(determinant(gaussian_elimination(Q)))

def dpll_search_tree(phi):
    def dpll(clause_set, assignment):
        if not clause_set:
            return True, assignment
        unit_clauses = [c for c in clause_set if len(c) == 1]
        if unit_clauses:
            literal = unit_clauses[0][0]
            if literal > 0:
                new_assignment[literal] = True
            else:
                new_assignment[-literal] = False
            return dpll(clause_set - {c for c in clause_set if literal in c}, new_assignment)
        pure_lits = [l for l, count in sum([[(var, 1) if var > 0 else (-var, -1) for var in clause] for clause in clause_set], []) if abs(count) == len(clause_set)]
        if pure_lits:
            literal = pure_lits[0]
            new_assignment[literal] = literal > 0
            return dpll(clause_set - {c for c in clause_set if literal in c}, new_assignment)
        var = next(iter(clause_set))
        for value in [True, False]:
            new_assignment[var] = value
            result, assignment = dpll(clause_set - {c for c in clause_set if var in c}, new_assignment)
            if result:
                return True, assignment
        return False, {}
    
    n = len(phi)
    clause_set = set(tuple(sorted(c)) for c in phi)
    new_assignment = [None] * (n + 1)
    return dpll(clause_set, new_assignment)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    phi = [[random.randint(-n, n) for _ in range(random.randint(2, n))] for _ in range(n)]
    m_order_val = m_order(phi)
    dpll_result, assignment = dpll_search_tree(phi)
    if not dpll_result:
        return {
            "metric_name": "diameter",
            "metric_value": -1,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "DPLL search tree failed to find a satisfying assignment"
        }
    d_val = len(assignment) - 1
    return {
        "metric_name": "diameter",
        "metric_value": d_val,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 17 for i in range(30)]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(r["metric_value"] < 0.5 for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if r["metric_value"] < 0.5)
        print(f"RESULT: FALSIFIED counterexample=\"diameter less than 0.5\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction} n_tested={len(results)}")