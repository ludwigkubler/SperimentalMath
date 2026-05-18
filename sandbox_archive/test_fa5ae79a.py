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

def generate_tseitin_cnf(n):
    variables = list(range(1, n + 1))
    clauses = []
    for i in range(0, n, 2):
        if i + 1 < n:
            clauses.append([variables[i], variables[i + 1], random.choice([-variables[i], -variables[i + 1]])])
    return clauses

def generate_trivial_unsat_cnf(n):
    variables = list(range(1, n + 1))
    clauses = []
    for i in range(n):
        clauses.append([variables[i], -variables[i]])
    return clauses

def is_satisfiable(clauses, assignment):
    for clause in clauses:
        satisfied = False
        for lit in clause:
            var = abs(lit)
            val = assignment[var]
            if (lit > 0 and val) or (lit < 0 and not val):
                satisfied = True
                break
        if not satisfied:
            return False
    return True

def dpll(clauses, assignment, variables, max_nodes=2000000):
    if max_nodes <= 0:
        return None
    if not clauses:
        return assignment
    for clause in clauses:
        if not clause:
            return None
    for clause in clauses:
        if len(clause) == 1:
            lit = clause[0]
            var = abs(lit)
            val = lit > 0
            new_assignment = assignment.copy()
            new_assignment[var] = val
            new_clauses = []
            for c in clauses:
                if lit not in c:
                    new_c = [l for l in c if -l not in c]
                    new_clauses.append(new_c)
            result = dpll(new_clauses, new_assignment, variables, max_nodes - 1)
            if result is not None:
                return result
            return None
    var = max(variables, key=lambda v: sum(1 for clause in clauses if v in clause or -v in clause))
    for val in [True, False]:
        new_assignment = assignment.copy()
        new_assignment[var] = val
        new_clauses = []
        for clause in clauses:
            if var not in [abs(l) for l in clause]:
                new_clauses.append(clause)
            else:
                new_c = [l for l in clause if abs(l) != var or (l > 0) != val]
                if new_c:
                    new_clauses.append(new_c)
        result = dpll(new_clauses, new_assignment, [v for v in variables if v != var], max_nodes - 1)
        if result is not None:
            return result
    return None

def compute_l1(clauses, n):
    l1 = 0.0
    for clause in clauses:
        for S in itertools.product([-1, 1], repeat=n):
            term = 1.0
            for lit in clause:
                var = abs(lit) - 1
                term *= S[var] if lit > 0 else -S[var]
            l1 += abs(term)
    return l1 / (2 ** n)

def run_trial(seed):
    random.seed(seed)
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    instances_tested = 0

    # Test Tseitin CNFs
    for n in [8, 10, 12, 14, 16, 18, 20]:
        clauses = generate_tseitin_cnf(n)
        m = len(clauses)
        if m == 0:
            continue
        variables = list(range(1, n + 1))
        assignment = dpll(clauses, {}, variables)
        if assignment is None:
            l1 = compute_l1(clauses, n)
            t_star = 2 * 10**6  # Assume worst case
            ratio = l1 / math.sqrt(m + 1)
            bound = 3 * math.sqrt(math.log2(t_star + 1) + 1)
            if ratio > bound:
                conjecture_holds = False
                counterexample = f"Tseitin CNF with n={n}, m={m}, L1={l1}, t*={t_star}"
                break
            metric_values.append(ratio)
            instances_tested += 1

    if not conjecture_holds:
        return {
            "metric_name": "L1 ratio",
            "metric_value": 0.0,
            "instances_tested": instances_tested,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        }

    # Test random 3-CNFs
    for n in [10, 15, 20, 25]:
        m = int(5.0 * n)
        clauses = generate_random_3cnf(n, m)
        variables = list(range(1, n + 1))
        assignment = dpll(clauses, {}, variables)
        if assignment is None:
            l1 = compute_l1(clauses, n)
            t_star = 2 * 10**6  # Assume worst case
            ratio = l1 / math.sqrt(m + 1)
            bound = 3 * math.sqrt(math.log2(t_star + 1) + 1)
            if ratio > bound:
                conjecture_holds = False
                counterexample = f"Random 3-CNF with n={n}, m={m}, L1={l1}, t*={t_star}"
                break
            metric_values.append(ratio)
            instances_tested += 1

    if not conjecture_holds:
        return {
            "metric_name": "L1 ratio",
            "metric_value": 0.0,
            "instances_tested": instances_tested,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        }

    # Test trivial-unsat CNFs
    for n in [5, 10, 15, 20]:
        clauses = generate_trivial_unsat_cnf(n)
        m = len(clauses)
        l1 = compute_l1(clauses, n)
        t_star = 1  # Trivial case
        ratio = l1 / math.sqrt(m + 1)
        bound = 3 * math.sqrt(math.log2(t_star + 1) + 1)
        if ratio > bound:
            conjecture_holds = False
            counterexample = f"Trivial-unsat CNF with n={n}, m={m}, L1={l1}, t*={t_star}"
            break
        metric_values.append(ratio)
        instances_tested += 1

    if not conjecture_holds:
        return {
            "metric_name": "L1 ratio",
            "metric_value": 0.0,
            "instances_tested": instances_tested,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        }

    if not metric_values:
        return {
            "metric_name": "L1 ratio",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No instances tested"
        }

    mean_metric = sum(metric_values) / len(metric_values)
    return {
        "metric_name": "L1 ratio",
        "metric_value": mean_metric,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    metric_values = []
    conjecture_holds_all = True
    counterexample = ""
    first_failing_seed = None

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        metric_values.append(result["metric_value"])
        if not result["conjecture_holds"]:
            conjecture_holds_all = False
            counterexample = result["counterexample"]
            first_failing_seed = seed
            break

    if not conjecture_holds_all:
        print(f'RESULT: FALSIFIED counterexample="{counterexample}" first_failing_seed={first_failing_seed}')
    else:
        mean_metric = sum(metric_values) / len(metric_values)
        std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
        support_fraction = sum(1 for x in metric_values if x <= 3.0) / len(metric_values)
        if support_fraction >= 0.8:
            print(f'RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}')
        else:
            print('RESULT: INCONCLUSIVE reason=insufficient_support')