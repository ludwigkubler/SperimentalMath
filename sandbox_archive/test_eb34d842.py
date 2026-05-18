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
    variables = list(range(n))
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, 3)
        sign = [random.choice([-1, 1]) for _ in range(3)]
        clauses.append([(sign[i], clause[i]) for i in range(3)])
    return clauses

def generate_tseitin_graph(v):
    edges = []
    for i in range(v):
        for j in range(i + 1, v):
            if random.random() < 0.5:
                edges.append((i, j))
    return edges

def generate_tseitin_cnf(v, edges):
    n = v + len(edges)
    clauses = []
    for i in range(v):
        for j in range(i + 1, v):
            if (i, j) in edges:
                clauses.append([(1, i), (1, j), (-1, v + edges.index((i, j)))])
                clauses.append([(-1, i), (-1, j), (-1, v + edges.index((i, j)))])
                clauses.append([(1, i), (-1, j), (1, v + edges.index((i, j)))])
                clauses.append([(-1, i), (1, j), (1, v + edges.index((i, j)))])
    return clauses

def generate_trivial_unsat(n, m):
    variables = list(range(n))
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, 3)
        sign = [random.choice([-1, 1]) for _ in range(3)]
        clauses.append([(sign[i], clause[i]) for i in range(3)])
    clauses.append([(1, 0), (1, 0), (1, 0)])
    return clauses

def is_satisfiable(clauses, assignment):
    for clause in clauses:
        satisfied = False
        for sign, var in clause:
            if (sign == 1 and assignment[var]) or (sign == -1 and not assignment[var]):
                satisfied = True
                break
        if not satisfied:
            return False
    return True

def dpll(clauses, assignment, variables, node_count):
    if node_count[0] > 2 * 10**6:
        return False, node_count[0]
    if not clauses:
        return True, node_count[0]
    for clause in clauses:
        if len(clause) == 1:
            sign, var = clause[0]
            if var in assignment:
                if (sign == 1 and not assignment[var]) or (sign == -1 and assignment[var]):
                    return False, node_count[0]
            else:
                new_assignment = assignment.copy()
                new_assignment[var] = (sign == 1)
                new_clauses = [c for c in clauses if c != clause]
                satisfied, node_count[0] = dpll(new_clauses, new_assignment, variables, node_count)
                if satisfied:
                    return True, node_count[0]
                return False, node_count[0]
    for var in variables:
        if var not in assignment:
            for value in [True, False]:
                new_assignment = assignment.copy()
                new_assignment[var] = value
                new_clauses = []
                for clause in clauses:
                    new_clause = [lit for lit in clause if lit[1] != var or (lit[0] == 1 and value) or (lit[0] == -1 and not value)]
                    if not new_clause:
                        break
                    new_clauses.append(new_clause)
                else:
                    satisfied, node_count[0] = dpll(new_clauses, new_assignment, variables, node_count)
                    if satisfied:
                        return True, node_count[0]
            return False, node_count[0]
    return False, node_count[0]

def compute_l1(clauses, n):
    l1 = 0.0
    for clause in clauses:
        for S in itertools.product([-1, 1], repeat=n):
            term = 1.0
            for sign, var in clause:
                term *= (1 + sign * S[var]) / 2
            l1 += abs(term)
    return l1

def run_trial(seed):
    random.seed(seed)
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    instances_tested = 0

    # Tseitin instances
    for v in [8, 10, 12, 14, 16, 18, 20]:
        edges = generate_tseitin_graph(v)
        clauses = generate_tseitin_cnf(v, edges)
        n = v + len(edges)
        m = len(clauses)
        if m == 0:
            continue
        l1 = compute_l1(clauses, n)
        node_count = [0]
        satisfied, nodes = dpll(clauses, {}, list(range(n)), node_count)
        if not satisfied:
            t_star = nodes
            ratio = l1 / math.sqrt(m + 1)
            bound = 3 * math.sqrt(math.log2(t_star + 1) + 1)
            if ratio > bound:
                conjecture_holds = False
                counterexample = f"Tseitin instance with v={v}, n={n}, m={m}, L1={l1}, t*={t_star}, ratio={ratio}, bound={bound}"
                break
            metric_values.append(ratio)
            instances_tested += 1

    if not conjecture_holds:
        return {
            "metric_name": "L1_ratio",
            "metric_value": 0.0,
            "instances_tested": instances_tested,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        }

    # Random unsat 3-CNF instances
    for n in [10, 15, 20, 25]:
        m = int(5.0 * n)
        clauses = generate_random_3cnf(n, m)
        node_count = [0]
        satisfied, nodes = dpll(clauses, {}, list(range(n)), node_count)
        if not satisfied:
            l1 = compute_l1(clauses, n)
            t_star = nodes
            ratio = l1 / math.sqrt(m + 1)
            bound = 3 * math.sqrt(math.log2(t_star + 1) + 1)
            if ratio > bound:
                conjecture_holds = False
                counterexample = f"Random unsat 3-CNF instance with n={n}, m={m}, L1={l1}, t*={t_star}, ratio={ratio}, bound={bound}"
                break
            metric_values.append(ratio)
            instances_tested += 1

    if not conjecture_holds:
        return {
            "metric_name": "L1_ratio",
            "metric_value": 0.0,
            "instances_tested": instances_tested,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        }

    # Trivial unsat instances
    for n in [5, 10, 15, 20]:
        m = 5
        clauses = generate_trivial_unsat(n, m)
        node_count = [0]
        satisfied, nodes = dpll(clauses, {}, list(range(n)), node_count)
        if not satisfied:
            l1 = compute_l1(clauses, n)
            t_star = nodes
            ratio = l1 / math.sqrt(m + 1)
            bound = 3 * math.sqrt(math.log2(t_star + 1) + 1)
            if ratio > bound:
                conjecture_holds = False
                counterexample = f"Trivial unsat instance with n={n}, m={m}, L1={l1}, t*={t_star}, ratio={ratio}, bound={bound}"
                break
            metric_values.append(ratio)
            instances_tested += 1

    if not conjecture_holds:
        return {
            "metric_name": "L1_ratio",
            "metric_value": 0.0,
            "instances_tested": instances_tested,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        }

    if not metric_values:
        return {
            "metric_name": "L1_ratio",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": True,
            "counterexample": ""
        }

    mean_metric = sum(metric_values) / len(metric_values)
    return {
        "metric_name": "L1_ratio",
        "metric_value": mean_metric,
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

    metric_values = [r["metric_value"] for r in results if r["metric_value"] != 0.0]
    if not metric_values:
        print("RESULT: INCONCLUSIVE reason=no_valid_instances")
        sys.exit(0)

    mean = sum(metric_values) / len(metric_values)
    variance = sum((x - mean) ** 2 for x in metric_values) / len(metric_values)
    std = math.sqrt(variance)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")