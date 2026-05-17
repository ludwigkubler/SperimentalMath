# auto-injected by SEC sandbox
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import itertools
from fractions import Fraction

def generate_3cnf(n, alpha):
    m = int(alpha * n)
    variables = list(range(n))
    clauses = []
    for _ in range(m):
        clause_vars = random.sample(variables, 3)
        clause = [(var, random.choice([True, False])) for var in clause_vars]
        clauses.append(clause)
    return clauses

def is_unsatisfiable(clauses, n):
    def dpll(clauses, assignment):
        if not clauses:
            return False
        for clause in clauses:
            if all(not (var in assignment and assignment[var] == lit) for var, lit in clause):
                return False
        for var in range(n):
            if var not in assignment:
                new_assignment = assignment.copy()
                new_assignment[var] = True
                if not dpll([c for c in clauses if not any((v, l) in new_assignment.items() and new_assignment[v] == l for v, l in c)], new_assignment):
                    new_assignment[var] = False
                    if not dpll([c for c in clauses if not any((v, l) in new_assignment.items() and new_assignment[v] == l for v, l in c)], new_assignment):
                        return False
                return True
        return True

    return dpll(clauses, {})

def build_clause_overlap_graph(clauses):
    graph = {}
    for i, clause in enumerate(clauses):
        graph[i] = set()
        for j, other_clause in enumerate(clauses):
            if i != j and any(var in [v for v, _ in other_clause] for var, _ in clause):
                graph[i].add(j)
    return graph

def compute_fixed_point(graph, m):
    mu = {v: Fraction(1, 1) for v in graph}
    for _ in range(500):
        new_mu = {}
        for v in graph:
            sum_mu = sum(mu[u] for u in graph[v])
            new_mu[v] = Fraction(1, 1 + sum_mu)
        if all(abs(mu[v] - new_mu[v]) < Fraction(1, 10**9) for v in graph):
            break
        mu = new_mu
    return mu

def compute_lambda(mu):
    return -sum(math.log2(float(mu[v])) for v in mu)

def count_dpll_leaves(clauses, n):
    def dpll_count(clauses, assignment):
        if not clauses:
            return 1
        count = 0
        for clause in clauses:
            if all(not (var in assignment and assignment[var] == lit) for var, lit in clause):
                return 0
        for var in range(n):
            if var not in assignment:
                new_assignment = assignment.copy()
                new_assignment[var] = True
                count += dpll_count([c for c in clauses if not any((v, l) in new_assignment.items() and new_assignment[v] == l for v, l in c)], new_assignment)
                new_assignment[var] = False
                count += dpll_count([c for c in clauses if not any((v, l) in new_assignment.items() and new_assignment[v] == l for v, l in c)], new_assignment)
                return count
        return 1

    return dpll_count(clauses, {})

def run_trial(seed):
    random.seed(seed)
    n_sizes = [10, 14, 18, 22, 26, 30, 34]
    alpha = 4.26
    instances_tested = 0
    metric_values = []
    conjecture_holds = True
    counterexample = ""

    for n in n_sizes:
        for _ in range(30):
            clauses = generate_3cnf(n, alpha)
            if not is_unsatisfiable(clauses, n):
                continue
            instances_tested += 1
            graph = build_clause_overlap_graph(clauses)
            mu = compute_fixed_point(graph, len(clauses))
            Lambda = compute_lambda(mu)
            if Lambda <= 0:
                continue
            t_star = count_dpll_leaves(clauses, n)
            if t_star <= 0:
                continue
            r = math.log2(t_star) / Lambda
            metric_values.append(r)
            if r < 0.125:
                conjecture_holds = False
                counterexample = f"n={n}, seed={seed}, r={r}"

    if not metric_values:
        return {
            "metric_name": "log2(t*(F))/Lambda(F)",
            "metric_value": 0.0,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }

    mean_r = sum(metric_values) / len(metric_values)
    return {
        "metric_name": "log2(t*(F))/Lambda(F)",
        "metric_value": mean_r,
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

    metric_values = [r["metric_value"] for r in results if r["metric_value"] > 0]
    if not metric_values:
        print("RESULT: INCONCLUSIVE reason=no_valid_instances")
        sys.exit(0)

    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if any(r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    elif support_fraction >= 0.8 and mean <= 0.5:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")