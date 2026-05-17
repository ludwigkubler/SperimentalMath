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
        if random.random() < 0.5:
            clause[0] = -clause[0]
        if random.random() < 0.5:
            clause[1] = -clause[1]
        if random.random() < 0.5:
            clause[2] = -clause[2]
        clauses.append(clause)
    return clauses

def is_unsatisfiable(clauses, n):
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
            return True
        for lit in clauses[0]:
            new_assignment = assignment.copy()
            new_assignment[lit] = True
            if dpll([c for c in clauses if lit not in c and -lit not in c], new_assignment):
                return True
        return False
    return not dpll(clauses, {})

def build_clause_overlap_graph(clauses):
    graph = defaultdict(set)
    for i, clause1 in enumerate(clauses):
        for j, clause2 in enumerate(clauses):
            if i != j and any(abs(lit1) == abs(lit2) for lit1 in clause1 for lit2 in clause2):
                graph[i].add(j)
    return graph

def compute_fixed_point(graph, m):
    mu = [1.0] * m
    for _ in range(500):
        new_mu = [0.0] * m
        for v in range(m):
            sum_mu = sum(mu[u] for u in graph[v])
            new_mu[v] = 1.0 / (1.0 + sum_mu)
        if all(abs(new_mu[v] - mu[v]) < 1e-9 for v in range(m)):
            break
        mu = new_mu
    return mu

def compute_lambda(mu):
    return -sum(math.log2(mu_v) for mu_v in mu)

def count_dpll_leaves(clauses, n):
    def dpll_count(clauses, assignment):
        if not clauses:
            return 1
        count = 0
        for clause in clauses:
            if all(lit in assignment for lit in clause):
                continue
            if any(-lit in assignment for lit in clause):
                continue
            break
        else:
            return 1
        for lit in clauses[0]:
            new_assignment = assignment.copy()
            new_assignment[lit] = True
            count += dpll_count([c for c in clauses if lit not in c and -lit not in c], new_assignment)
        return count
    return dpll_count(clauses, {})

def run_trial(seed):
    random.seed(seed)
    n_values = [10, 14, 18, 22, 26, 30, 34]
    alpha = 4.26
    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        clauses = generate_3cnf(n, alpha)
        if not is_unsatisfiable(clauses, n):
            continue
        graph = build_clause_overlap_graph(clauses)
        m = len(clauses)
        mu = compute_fixed_point(graph, m)
        lambda_f = compute_lambda(mu)
        t_star = count_dpll_leaves(clauses, n)
        if t_star == 0:
            continue
        r = math.log2(t_star) / lambda_f
        metric_values.append(r)
        instances_tested += 1
        if r < 0.125:
            conjecture_holds = False
            counterexample = f"n={n}, seed={seed}, r={r}"

    if not metric_values:
        return {
            "metric_name": "r(F)",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }

    mean_r = sum(metric_values) / len(metric_values)
    min_r = min(metric_values)

    return {
        "metric_name": "r(F)",
        "metric_value": mean_r,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds and min_r >= 0.125 and mean_r <= 0.5,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    metric_values = [r["metric_value"] for r in results if r["instances_tested"] > 0]
    if not metric_values:
        print("RESULT: INCONCLUSIVE reason=no_valid_instances")
        sys.exit(0)

    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if any(r["counterexample"] for r in results):
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        first_failing_seed = next(r["seed"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")