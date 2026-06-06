# auto-injected by SEC sandbox
import math
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
from fractions import Fraction
from itertools import combinations, product

def generate_cnf(n, m):
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause = [random.choice(variables) * (-1 if random.randint(0, 1) else 1)]
        while len(clause) < 3 and any(x == y or x == -y for x in clause):
            new_var = random.choice(variables)
            if new_var not in clause:
                clause.append(new_var * (-1 if random.randint(0, 1) else 1))
        clauses.append(clause)
    return clauses

def dpll_solve(cnf):
    def is_satisfiable(vars):
        for clause in cnf:
            if all(var not in vars and -var not in vars for var in clause):
                return False
        return True

    def backtrack(vars, assignment):
        if len(assignment) == n:
            return is_satisfiable(assignment)
        var = list(set(range(1, n + 1)) - set(assignment.keys()))[0]
        for val in [True, False]:
            assignment[var] = val
            if backtrack(vars, assignment):
                return True
            del assignment[var]
        return False

    assignment = {}
    return backtrack(variables, assignment)

def quiver_representation(cnf):
    n = len(cnf)
    Q = [[0] * n for _ in range(n)]
    for clause in cnf:
        for var1 in clause:
            for var2 in clause:
                if var1 != var2:
                    Q[abs(var1) - 1][abs(var2) - 1] += 1
    return Q

def min_order(Q):
    n = len(Q)
    visited = [False] * n
    order = 0

    def dfs(v):
        nonlocal order
        stack = [v]
        while stack:
            u = stack.pop()
            if not visited[u]:
                visited[u] = True
                for v in range(n):
                    if Q[u][v] > 0 and not visited[v]:
                        stack.append(v)
                order += 1

    dfs(0)
    return order

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []

    for n in n_values:
        m = 2 * n  # Ensure at least one clause per variable
        cnf = generate_cnf(n, m)
        Q = quiver_representation(cnf)
        min_order_Q = min_order(Q)
        l_phi = dpll_solve(cnf)

        if l_phi is None:
            continue

        results.append({
            "n": n,
            "min_order_Q": min_order_Q,
            "l_phi": l_phi
        })

    if not results:
        return {
            "metric_name": "log(min_order(Q(φ))) vs. DPLL proof path length",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid CNF formulas generated"
        }

    log_min_order_Q = [Fraction(math.log(result["min_order_Q"]), math.e) for result in results]
    l_phi_values = [result["l_phi"] for result in results]

    correlation_coefficient = sum((x - mean_x) * (y - mean_y) for x, y in zip(log_min_order_Q, l_phi_values)) / \
                               (math.sqrt(sum((x - mean_x) ** 2 for x in log_min_order_Q)) *
                                math.sqrt(sum((y - mean_y) ** 2 for y in l_phi_values)))

    mean_metric_value = correlation_coefficient
    std_metric_value = 0.0
    conjecture_holds = all(0.6 <= corr < 0.7 for corr in log_min_order_Q)
    counterexample = "" if conjecture_holds else "Correlation coefficient outside [0.6, 0.7] range"

    return {
        "metric_name": "log(min_order(Q(φ))) vs. DPLL proof path length",
        "metric_value": mean_metric_value,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []

    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")

        if "metric_value" in trial_result and trial_result["metric_value"] is not None:
            results.append(trial_result["metric_value"])

    mean_metric_value = sum(results) / len(results) if results else 0
    std_metric_value = math.sqrt(sum((x - mean_metric_value) ** 2 for x in results)) / len(results) if results else 0
    support_fraction = sum(1 for result in results if 0.6 <= result < 0.7) / len(results)

    if all(0.6 <= result < 0.7 for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(result < 0.6 or result >= 0.7 for result in results):
        first_failing_seed = seeds[next(i for i, result in enumerate(results) if not (0.6 <= result < 0.7))]
        print(f"RESULT: FALSIFIED counterexample='Correlation coefficient outside [0.6, 0.7] range' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE Reason=No valid CNF formulas generated")