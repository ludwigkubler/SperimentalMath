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

def generate_unsat_3cnf(n, alpha, seed):
    random.seed(seed)
    m = int(alpha * n)
    variables = list(range(1, n + 1))
    clauses = []

    while len(clauses) < m:
        clause = random.sample(variables, 3)
        negated = [random.choice([-1, 1]) * v for v in clause]
        if negated not in clauses:
            clauses.append(negated)

    # Ensure unsatisfiability by adding a contradiction
    if len(clauses) >= 2:
        clauses[-1] = [-clauses[0][0], -clauses[0][1], -clauses[0][2]]

    return clauses

def build_clause_sharing_graph(clauses):
    graph = defaultdict(set)
    for i, clause in enumerate(clauses):
        for j, other_clause in enumerate(clauses):
            if i != j and any(abs(v) in [abs(x) for x in other_clause] for v in clause):
                graph[i].add(j)
    return graph

def compute_dismantlability_defect(graph):
    delta = 0
    remaining = set(graph.keys())

    while remaining:
        found = False
        for v in list(remaining):
            neighbors = graph[v]
            if all(len(graph[u] & remaining) <= 1 for u in neighbors):
                remaining.remove(v)
                found = True
                break
        if not found:
            delta += len(remaining)
            break

    return delta

def dpll(clauses, assignments, decision_nodes):
    decision_nodes[0] += 1
    for clause in clauses:
        satisfied = False
        for lit in clause:
            if (lit > 0 and assignments.get(abs(lit), False)) or (lit < 0 and not assignments.get(abs(lit), False)):
                satisfied = True
                break
        if not satisfied:
            return False

    for var in range(1, max(abs(lit) for clause in clauses for lit in clause) + 1):
        if var not in assignments:
            assignments[var] = True
            if dpll(clauses, assignments, decision_nodes):
                return True
            assignments[var] = False
            if dpll(clauses, assignments, decision_nodes):
                return True
            del assignments[var]
            return False

    return True

def run_trial(seed):
    n_values = [12, 16, 20, 24, 28, 32, 36, 40]
    alpha_values = [4.5, 5.0, 5.5]
    results = []

    for n in n_values:
        for alpha in alpha_values:
            clauses = generate_unsat_3cnf(n, alpha, seed)
            m = len(clauses)
            graph = build_clause_sharing_graph(clauses)
            delta = compute_dismantlability_defect(graph)

            decision_nodes = [0]
            assignments = {}
            dpll(clauses, assignments, decision_nodes)
            t_star = decision_nodes[0]

            if delta == 0:
                ratio = 0
            else:
                ratio = 8 * m * math.log2(t_star + 1) / (n * delta)

            results.append({
                "n": n,
                "alpha": alpha,
                "m": m,
                "delta": delta,
                "t_star": t_star,
                "ratio": ratio
            })

    min_ratio = min(result["ratio"] for result in results)
    conjecture_holds = min_ratio >= 1.0

    return {
        "metric_name": "min_ratio",
        "metric_value": min_ratio,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": f"min_ratio={min_ratio}" if not conjecture_holds else ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]

    metric_values = []
    conjecture_holds_counts = 0
    total_trials = 0

    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        metric_values.append(trial["metric_value"])
        if trial["conjecture_holds"]:
            conjecture_holds_counts += 1
        total_trials += 1

    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = conjecture_holds_counts / total_trials

    if all(trial["conjecture_holds"] for trial in [run_trial(seed) for seed in seeds]):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        counterexample = next(trial["counterexample"] for trial in [run_trial(seed) for seed in seeds] if not trial["conjecture_holds"])
        first_failing_seed = next(seed for seed in seeds if not run_trial(seed)["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample={counterexample} first_failing_seed={first_failing_seed}")