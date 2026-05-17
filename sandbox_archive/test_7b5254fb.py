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
    for edge in edges:
        u, v = edge
        clauses.append([u, v, random.choice([-u, -v])])
    if odd_charge:
        clauses.append([random.choice(variables)])
    return clauses

def is_unsat(clauses, n):
    assignments = {}
    for clause in clauses:
        for lit in clause:
            var = abs(lit)
            if var not in assignments:
                assignments[var] = random.choice([True, False])
    for clause in clauses:
        satisfied = False
        for lit in clause:
            var = abs(lit)
            val = assignments[var]
            if (lit > 0 and val) or (lit < 0 and not val):
                satisfied = True
                break
        if not satisfied:
            return True
    return False

def minimax(clauses, n, player, memo):
    key = (tuple(sorted(clauses)), player)
    if key in memo:
        return memo[key]
    assignments = {}
    for clause in clauses:
        for lit in clause:
            var = abs(lit)
            if var not in assignments:
                assignments[var] = None
    if len(assignments) == n:
        score = 0
        for clause in clauses:
            satisfied = False
            for lit in clause:
                var = abs(lit)
                val = assignments[var]
                if (lit > 0 and val) or (lit < 0 and not val):
                    satisfied = True
                    break
            if not satisfied:
                score += 1
        memo[key] = score
        return score
    if player == 'Maximizer':
        max_score = -float('inf')
        for var in assignments:
            if assignments[var] is None:
                for val in [True, False]:
                    new_assignments = assignments.copy()
                    new_assignments[var] = val
                    new_clauses = []
                    for clause in clauses:
                        new_clause = []
                        for lit in clause:
                            if abs(lit) != var:
                                new_clause.append(lit)
                        if new_clause:
                            new_clauses.append(new_clause)
                    score = minimax(new_clauses, n, 'Minimizer', memo)
                    max_score = max(max_score, score)
        memo[key] = max_score
        return max_score
    else:
        min_score = float('inf')
        for var in assignments:
            if assignments[var] is None:
                for val in [True, False]:
                    new_assignments = assignments.copy()
                    new_assignments[var] = val
                    new_clauses = []
                    for clause in clauses:
                        new_clause = []
                        for lit in clause:
                            if abs(lit) != var:
                                new_clause.append(lit)
                        if new_clause:
                            new_clauses.append(new_clause)
                    score = minimax(new_clauses, n, 'Maximizer', memo)
                    min_score = min(min_score, score)
        memo[key] = min_score
        return min_score

def tree_dpll(clauses, n, order, memo):
    key = (tuple(sorted(clauses)), tuple(order))
    if key in memo:
        return memo[key]
    if not clauses:
        memo[key] = (True, 0)
        return (True, 0)
    if any(len(clause) == 0 for clause in clauses):
        memo[key] = (False, 0)
        return (False, 0)
    if not order:
        memo[key] = (True, 0)
        return (True, 0)
    var = order[0]
    new_order = order[1:]
    max_width = 0
    for val in [True, False]:
        new_clauses = []
        for clause in clauses:
            new_clause = []
            for lit in clause:
                if abs(lit) != var:
                    new_clause.append(lit)
                elif (lit > 0 and val) or (lit < 0 and not val):
                    break
            else:
                if new_clause:
                    new_clauses.append(new_clause)
        result, width = tree_dpll(new_clauses, n, new_order, memo)
        if result:
            max_width = max(max_width, width + 1)
    memo[key] = (True, max_width)
    return (True, max_width)

def run_trial(seed):
    random.seed(seed)
    n_values = [8, 10, 12, 14]
    v_values = [6, 8, 10]
    instances_tested = 0
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    for n in n_values:
        m = int(math.ceil(4.5 * n))
        clauses = generate_random_3cnf(n, m)
        if is_unsat(clauses, n):
            memo = {}
            L = minimax(clauses, n, 'Maximizer', memo)
            R = minimax(clauses, n, 'Minimizer', memo)
            t = (L - R) / 2
            order = list(range(1, n + 1))
            memo = {}
            _, w = tree_dpll(clauses, n, order, memo)
            if t > 5 * w:
                conjecture_holds = False
                counterexample = f"Random 3-CNF with n={n}, t={t}, w={w}"
                break
            metric_values.append(t / w)
            instances_tested += 1
    if conjecture_holds:
        for v in v_values:
            odd_charge = random.choice([True, False])
            clauses = generate_tseitin_formula(v, odd_charge)
            if is_unsat(clauses, v):
                memo = {}
                L = minimax(clauses, v, 'Maximizer', memo)
                R = minimax(clauses, v, 'Minimizer', memo)
                t = (L - R) / 2
                if t < 0.3 * v:
                    conjecture_holds = False
                    counterexample = f"Tseitin formula with v={v}, t={t}"
                    break
                metric_values.append(t / v)
                instances_tested += 1
    metric_value = sum(metric_values) / len(metric_values) if metric_values else 0
    return {
        "metric_name": "temperature_to_width_ratio",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    metric_values = []
    conjecture_holds_counts = 0
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        metric_values.append(result["metric_value"])
        if result["conjecture_holds"]:
            conjecture_holds_counts += 1
    mean_metric = sum(metric_values) / len(metric_values) if metric_values else 0
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values)) if metric_values else 0
    support_fraction = conjecture_holds_counts / len(seeds)
    if support_fraction == 1:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif support_fraction < 0.8:
        print(f"RESULT: FALSIFIED counterexample={result['counterexample']} first_failing_seed={seeds[conjecture_holds_counts]}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")