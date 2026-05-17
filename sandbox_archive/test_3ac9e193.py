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
        clauses.append(clause)
    return clauses

def generate_tseitin_formula(v, odd_charge):
    variables = list(range(1, v + 1))
    edges = []
    for i in range(v):
        for j in range(i + 1, v):
            if random.random() < 0.5:
                edges.append((i + 1, j + 1))
    clauses = []
    for i, j in edges:
        clauses.append([i, j, -(v + len(edges) + 1)])
        clauses.append([-i, j, -(v + len(edges) + 1)])
        clauses.append([i, -j, -(v + len(edges) + 1)])
        clauses.append([-i, -j, -(v + len(edges) + 1)])
    if odd_charge:
        clauses.append([random.choice(variables)])
    return clauses

def is_unsat(clauses, n):
    def dpll(clauses, assignment):
        if not clauses:
            return True
        for clause in clauses:
            if all(lit in assignment for lit in clause):
                continue
            if any(-lit in assignment for lit in clause):
                continue
            break
        else:
            return False
        for lit in clause:
            if -lit not in assignment:
                new_assignment = assignment.copy()
                new_assignment.add(lit)
                if dpll([c for c in clauses if c != clause], new_assignment):
                    return True
        return False
    return not dpll(clauses, set())

def memoized_minimax(clauses, n, assignment, memo):
    key = tuple(sorted(assignment))
    if key in memo:
        return memo[key]
    if len(assignment) == n:
        score = sum(1 for clause in clauses if all(-lit in assignment for lit in clause))
        memo[key] = score
        return score
    current_player = len(assignment) % 2
    best_score = -math.inf if current_player == 0 else math.inf
    for var in range(1, n + 1):
        if var not in assignment and -var not in assignment:
            new_assignment = assignment.copy()
            new_assignment.add(var)
            score = memoized_minimax(clauses, n, new_assignment, memo)
            if current_player == 0:
                best_score = max(best_score, score)
            else:
                best_score = min(best_score, score)
    memo[key] = best_score
    return best_score

def compute_temperature(clauses, n):
    memo = {}
    L = memoized_minimax(clauses, n, set(), memo)
    memo = {}
    R = memoized_minimax(clauses, n, set(), memo)
    return (L - R) / 2

def compute_width(clauses, n):
    def tree_dp(clauses, n, assignment, memo):
        key = tuple(sorted(assignment))
        if key in memo:
            return memo[key]
        if len(assignment) == n:
            score = sum(1 for clause in clauses if all(-lit in assignment for lit in clause))
            memo[key] = (score, [])
            return (score, [])
        current_player = len(assignment) % 2
        best_score = -math.inf if current_player == 0 else math.inf
        best_order = []
        for var in range(1, n + 1):
            if var not in assignment and -var not in assignment:
                new_assignment = assignment.copy()
                new_assignment.add(var)
                score, order = tree_dp(clauses, n, new_assignment, memo)
                if current_player == 0 and score > best_score:
                    best_score = score
                    best_order = [var] + order
                elif current_player == 1 and score < best_score:
                    best_score = score
                    best_order = [var] + order
        memo[key] = (best_score, best_order)
        return (best_score, best_order)
    memo = {}
    _, order = tree_dp(clauses, n, set(), memo)
    width = 0
    for i in range(len(order)):
        width = max(width, len(set(order[:i+1])))
    return width

def run_trial(seed):
    random.seed(seed)
    n_values = [8, 10, 12, 14]
    v_values = [6, 8, 10]
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    instances_tested = 0

    for n in n_values:
        m = int(math.ceil(4.5 * n))
        clauses = generate_random_3cnf(n, m)
        if not is_unsat(clauses, n):
            continue
        t = compute_temperature(clauses, n)
        w = compute_width(clauses, n)
        metric_values.append(t / w)
        if t > 5 * w:
            conjecture_holds = False
            counterexample = f"Random 3-CNF with n={n} has t={t} > 5*w={5*w}"
            break
        instances_tested += 1

    if conjecture_holds:
        for v in v_values:
            odd_charge = random.choice([True, False])
            clauses = generate_tseitin_formula(v, odd_charge)
            t = compute_temperature(clauses, v)
            metric_values.append(t / v)
            if t < 0.3 * v:
                conjecture_holds = False
                counterexample = f"Tseitin formula with v={v} has t={t} < 0.3*v={0.3*v}"
                break
            instances_tested += 1

    return {
        "metric_name": "temperature_to_width_ratio",
        "metric_value": sum(metric_values) / len(metric_values) if metric_values else 0,
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

    metric_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    mean_metric = sum(metric_values) / len(metric_values) if metric_values else 0
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values)) if metric_values else 0
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")