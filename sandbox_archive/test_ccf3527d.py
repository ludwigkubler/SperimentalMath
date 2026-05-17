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

def generate_3cnf(n, alpha):
    m = int(alpha * n)
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, 3)
        if random.choice([True, False]):
            clause[0] = -clause[0]
        if random.choice([True, False]):
            clause[1] = -clause[1]
        if random.choice([True, False]):
            clause[2] = -clause[2]
        clauses.append(clause)
    return clauses

def is_unsatisfiable(clauses):
    n = max(max(abs(lit) for lit in clause) for clause in clauses)
    assignments = [None] * (n + 1)

    def dpll(clauses, assignments):
        if not clauses:
            return True
        if any(not clause for clause in clauses):
            return False

        for clause in clauses:
            if len(clause) == 1:
                lit = clause[0]
                var = abs(lit)
                if assignments[var] is not None and assignments[var] != (lit > 0):
                    return False
                assignments[var] = lit > 0
                new_clauses = [c for c in clauses if lit not in c]
                new_clauses = [[l for l in c if l != -lit] for c in new_clauses]
                if dpll(new_clauses, assignments.copy()):
                    return True
                assignments[var] = None
                return False

        var = max(range(1, n + 1), key=lambda v: sum(1 for clause in clauses if v in clause or -v in clause))
        for val in [True, False]:
            assignments[var] = val
            new_clauses = [c for c in clauses if var not in c and -var not in c]
            new_clauses = [[l for l in c if l != (var if val else -var)] for c in new_clauses]
            if dpll(new_clauses, assignments.copy()):
                return True
            assignments[var] = None
        return False

    return not dpll(clauses, assignments)

def build_clause_overlap_graph(clauses):
    graph = defaultdict(set)
    for i, clause1 in enumerate(clauses):
        for j, clause2 in enumerate(clauses):
            if i != j and any(lit in clause2 or -lit in clause2 for lit in clause1):
                graph[i].add(j)
    return graph

def compute_fixed_point(graph, m):
    mu = [1.0] * m
    for _ in range(500):
        new_mu = [0.0] * m
        for v in range(m):
            sum_neighbors = sum(mu[u] for u in graph[v])
            new_mu[v] = 1.0 / (1.0 + sum_neighbors)
        if max(abs(new_mu[v] - mu[v]) for v in range(m)) < 1e-9:
            break
        mu = new_mu
    return mu

def compute_lambda(mu):
    return -sum(math.log2(mu_v) for mu_v in mu)

def count_dpll_leaves(clauses):
    n = max(max(abs(lit) for lit in clause) for clause in clauses)
    assignments = [None] * (n + 1)

    def dpll_count(clauses, assignments):
        if not clauses:
            return 1
        if any(not clause for clause in clauses):
            return 0

        for clause in clauses:
            if len(clause) == 1:
                lit = clause[0]
                var = abs(lit)
                if assignments[var] is not None and assignments[var] != (lit > 0):
                    return 0
                assignments[var] = lit > 0
                new_clauses = [c for c in clauses if lit not in c]
                new_clauses = [[l for l in c if l != -lit] for c in new_clauses]
                return dpll_count(new_clauses, assignments.copy())

        var = max(range(1, n + 1), key=lambda v: sum(1 for clause in clauses if v in clause or -v in clause))
        count = 0
        for val in [True, False]:
            assignments[var] = val
            new_clauses = [c for c in clauses if var not in c and -var not in c]
            new_clauses = [[l for l in c if l != (var if val else -var)] for c in new_clauses]
            count += dpll_count(new_clauses, assignments.copy())
            assignments[var] = None
        return count

    return dpll_count(clauses, assignments)

def run_trial(seed):
    random.seed(seed)
    n_sizes = [10, 14, 18, 22, 26, 30, 34]
    alpha = 4.26
    results = []

    for n in n_sizes:
        clauses = generate_3cnf(n, alpha)
        if not is_unsatisfiable(clauses):
            continue

        graph = build_clause_overlap_graph(clauses)
        m = len(clauses)
        mu = compute_fixed_point(graph, m)
        Lambda = compute_lambda(mu)
        t_star = count_dpll_leaves(clauses)

        if Lambda <= 0:
            continue

        r = math.log2(t_star) / Lambda
        results.append(r)

    if not results:
        return {
            "metric_name": "r(F)",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }

    min_r = min(results)
    mean_r = sum(results) / len(results)
    conjecture_holds = min_r >= 0.125 and mean_r <= 0.5
    counterexample = "" if conjecture_holds else f"min_r={min_r} < 0.125"

    return {
        "metric_name": "r(F)",
        "metric_value": mean_r,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    metric_values = []
    conjecture_holds_counts = 0
    counterexamples = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        metric_values.append(result["metric_value"])
        if result["conjecture_holds"]:
            conjecture_holds_counts += 1
        if result["counterexample"]:
            counterexamples.append(result["counterexample"])

    mean_metric = sum(metric_values) / len(metric_values) if metric_values else 0.0
    std_metric = (sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values)) ** 0.5 if metric_values else 0.0
    support_fraction = conjecture_holds_counts / len(seeds) if seeds else 0.0

    if counterexamples:
        print(f"RESULT: FALSIFIED counterexample={counterexamples[0]} first_failing_seed={seeds[counterexamples.index(counterexamples[0])]}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")