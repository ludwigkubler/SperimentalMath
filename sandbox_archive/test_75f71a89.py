# auto-injected by SEC sandbox
import json
import os
import time
import re
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import itertools
from collections import defaultdict

def generate_random_3cnf(n, m):
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, 3)
        for i in range(3):
            if random.random() < 0.5:
                clause[i] = -clause[i]
        clauses.append(tuple(clause))
    return clauses

def generate_tseitin_formula(v, odd_charge=True):
    variables = list(range(1, v + 1))
    edges = []
    for i in range(v):
        for j in range(i + 1, v):
            if random.random() < 0.5:
                edges.append((variables[i], variables[j]))
    if odd_charge:
        if len(edges) % 2 == 0:
            edges.append((variables[0], variables[1]))
    clauses = []
    for u, v in edges:
        new_var = max(variables) + 1
        variables.append(new_var)
        clauses.append((u, v, -new_var))
        clauses.append((u, -v, new_var))
        clauses.append((-u, v, new_var))
        clauses.append((-u, -v, -new_var))
    return clauses

def is_unsat(clauses):
    n = max(abs(lit) for clause in clauses for lit in clause)
    assignments = {}

    def backtrack():
        if len(assignments) == n:
            return not any(all(assignments.get(abs(lit), False) == (lit < 0) for lit in clause) for clause in clauses)
        var = min(set(range(1, n + 1)) - set(abs(lit) for lit in assignments))
        for val in [True, False]:
            assignments[var] = val
            if backtrack():
                return True
            del assignments[var]
        return False

    return backtrack()

def minimax(clauses, player='max'):
    n = max(abs(lit) for clause in clauses for lit in clause)
    memo = {}

    def evaluate(assignments):
        if len(assignments) == n:
            return sum(1 for clause in clauses if all(assignments.get(abs(lit), False) == (lit < 0) for lit in clause))
        key = (tuple(sorted(assignments.items())), player)
        if key in memo:
            return memo[key]
        var = min(set(range(1, n + 1)) - set(abs(lit) for lit in assignments))
        if player == 'max':
            best = -float('inf')
            for val in [True, False]:
                new_assignments = assignments.copy()
                new_assignments[var] = val
                best = max(best, evaluate(new_assignments))
            memo[key] = best
            return best
        else:
            best = float('inf')
            for val in [True, False]:
                new_assignments = assignments.copy()
                new_assignments[var] = val
                best = min(best, evaluate(new_assignments))
            memo[key] = best
            return best

    return evaluate({})

def tree_dpll(clauses):
    n = max(abs(lit) for clause in clauses for lit in clause)
    memo = {}

    def solve(assignments):
        if len(assignments) == n:
            return not any(all(assignments.get(abs(lit), False) == (lit < 0) for lit in clause) for clause in clauses)
        key = tuple(sorted(assignments.items()))
        if key in memo:
            return memo[key]
        var = min(set(range(1, n + 1)) - set(abs(lit) for lit in assignments))
        result = False
        for val in [True, False]:
            new_assignments = assignments.copy()
            new_assignments[var] = val
            if solve(new_assignments):
                result = True
                break
        memo[key] = result
        return result

    return solve({})

def run_trial(seed):
    random.seed(seed)
    n_values = [8, 10, 12, 14]
    v_values = [6, 8, 10]
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        m = int(math.ceil(4.5 * n))
        clauses = generate_random_3cnf(n, m)
        if not is_unsat(clauses):
            continue
        instances_tested += 1
        L = minimax(clauses, 'max')
        R = minimax(clauses, 'min')
        t = (L - R) / 2
        w_star = tree_dpll(clauses)
        if t > 5 * w_star:
            conjecture_holds = False
            counterexample = f"Random 3-CNF with n={n} violated t(F) ≤ 5·w*(F): t={t}, w*={w_star}"
            break

    if conjecture_holds:
        for v in v_values:
            clauses = generate_tseitin_formula(v)
            if not is_unsat(clauses):
                continue
            instances_tested += 1
            L = minimax(clauses, 'max')
            R = minimax(clauses, 'min')
            t = (L - R) / 2
            if t < 0.3 * v:
                conjecture_holds = False
                counterexample = f"Tseitin formula with v={v} violated t(F) ≥ 0.3·v: t={t}, v={v}"
                break

    return {
        "metric_name": "temperature_to_width_ratio",
        "metric_value": t / w_star if conjecture_holds else 0,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    metric_values = [r["metric_value"] for r in results if r["conjecture_holds"]]
    if metric_values:
        mean = sum(metric_values) / len(metric_values)
        std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    else:
        mean = std = 0

    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={seeds[results.index(r)]}")
                break