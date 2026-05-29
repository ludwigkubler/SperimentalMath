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
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, m):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def matrix_multiply(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def dpll(variables, assignment):
    clauses = [
        [1, -2], [-1, 3], [2, 3],
        [-1, -2], [1, 2], [-1, 3]
    ]
    unsatisfied_clauses = [c for c in clauses if any(v in assignment and assignment[v] == True or -v in assignment and assignment[v] == False for v in c)]
    if not unsatisfied_clauses:
        return len(assignment)
    unit_clause = next((c for c in clauses if len(c) == 1), None)
    if unit_clause:
        v = abs(unit_clause[0])
        if v not in assignment:
            assignment[v] = unit_clause[0] > 0
            return dpll(variables, assignment)
    pure_literal = next((v for v in variables if all(v not in assignment and -v not in assignment for c in clauses)), None)
    if pure_literal is not None:
        assignment[pure_literal] = True
        return dpll(variables, assignment)
    v = random.choice(variables)
    assignment[v] = True
    depth_true = dpll(variables, assignment)
    assignment[v] = False
    depth_false = dpll(variables, assignment)
    return max(depth_true, depth_false)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    k = random.randint(2, min(n-1, 3))
    variables = list(range(1, n+1))
    clauses = []
    for _ in range(k):
        clause = [random.choice([-v, v]) for v in random.sample(variables, random.randint(1, n))]
        clauses.append(clause)
    
    depth = dpll(variables, {})
    expected_depth = 2 * n * math.log(n)
    metric_value = abs(depth - expected_depth)
    instances_tested = 1
    conjecture_holds = metric_value <= 3 * expected_depth
    counterexample = "" if conjecture_holds else f"Depth {depth} exceeds expected {expected_depth}"
    
    return {
        "metric_name": "DPLL Tree Depth",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Depth exceeds expected\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")