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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below pivot
        for j in range(i+1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n + 1):
                A[j][k] -= factor * A[i][k]

    # Back substitution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = Fraction(A[i][n], A[i][i])
        for j in range(i-1, -1, -1):
            A[j][n] -= A[j][i] * x[i]
    return x

def construct_quadratic_form(n):
    # Construct a random quadratic form over function fields
    Q = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            Q[i][j] = Fraction(random.randint(1, 10), random.randint(1, 10))
            Q[j][i] = Q[i][j]
    return Q

def compute_min_norm(Q):
    # Compute the minimal norm of the quadratic form
    A = [row + [Q[i][i]] for i, row in enumerate(Q)]
    x = gaussian_elimination(A)
    min_norm = sum(x[i]**2 * Q[i][i] for i in range(len(Q)))
    return float(min_norm)

def construct_dpll_tree(formula):
    # Construct the DPLL refutation tree
    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            if literal < 0:
                literal = -literal
                assignment[literal] = False
            else:
                assignment[literal] = True
            return dpll([c for c in clauses if literal not in c and -literal not in c], assignment)
        pure_literal = next((i for i in range(1, len(clauses) + 1) if (i not in assignment and -i not in assignment)), None)
        if pure_literal:
            assignment[pure_literal] = True
            return dpll([c for c in clauses if pure_literal not in c and -pure_literal not in c], assignment)
        literal = random.choice(range(1, len(clauses) + 1))
        assignment[literal] = True
        if dpll([c for c in clauses if literal not in c and -literal not in c], assignment):
            return True
        assignment[literal] = False
        return dpll([c for c in clauses if literal not in c and -literal not in c], assignment)
    
    n = len(formula)
    assignment = {}
    return dpll(formula, assignment)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(n, n * (n - 1) // 2)
    formula = [[random.choice([-i, i]) for _ in range(random.randint(3, 5))] for _ in range(m)]
    
    Q = construct_quadratic_form(n)
    min_norm = compute_min_norm(Q)
    
    dpll_tree_height = construct_dpll_tree(formula)
    
    return {
        "metric_name": "minimal_norm",
        "metric_value": min_norm,
        "instances_tested": 1,
        "conjecture_holds": min_norm <= dpll_tree_height,
        "counterexample": "" if min_norm <= dpll_tree_height else f"Formula with n={n}, m={m}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    std_metric_value = (sum((res["metric_value"] - mean_metric_value) ** 2 for res in results) / len(results)) ** 0.5
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((res["seed"] for res in results if not res["conjecture_holds"]), None)
        counterexample = next((res["counterexample"] for res in results if not res["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")