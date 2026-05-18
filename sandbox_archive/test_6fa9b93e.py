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

def generate_3cnf(n, m):
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, 3)
        if random.random() < 0.5:
            clause = [-x for x in clause]
        clauses.append(clause)
    return clauses

def is_unsatisfiable(clauses, max_steps=1000):
    n = max(abs(lit) for clause in clauses for lit in clause)
    assignments = {}
    steps = 0
    while steps < max_steps:
        steps += 1
        satisfied = True
        for clause in clauses:
            if not any((lit > 0 and assignments.get(lit, False)) or (lit < 0 and not assignments.get(-lit, True)) for lit in clause):
                satisfied = False
                break
        if satisfied:
            return False
        unsatisfied_clauses = [clause for clause in clauses if not any((lit > 0 and assignments.get(lit, False)) or (lit < 0 and not assignments.get(-lit, True)) for lit in clause)]
        if not unsatisfied_clauses:
            return True
        clause = random.choice(unsatisfied_clauses)
        lit = random.choice(clause)
        assignments[abs(lit)] = lit > 0
    return True

def build_clause_sharing_graph(clauses):
    graph = defaultdict(set)
    for i, clause in enumerate(clauses):
        for j, other_clause in enumerate(clauses):
            if i != j and any(abs(lit) in [abs(l) for l in other_clause] for lit in clause):
                graph[i].add(j)
    return graph

def compute_dismantlability_defect(graph):
    if not graph:
        return 0
    vertices = set(graph.keys())
    while True:
        dominated = False
        for v in list(vertices):
            neighbors = graph[v]
            if all(any(u in graph[w] for w in vertices if w != u) for u in neighbors):
                vertices.remove(v)
                dominated = True
                break
        if not dominated:
            break
    return len(vertices)

def count_dpll_decisions(clauses, max_steps=1000):
    n = max(abs(lit) for clause in clauses for lit in clause)
    assignments = {}
    decisions = 0
    steps = 0
    while steps < max_steps:
        steps += 1
        satisfied = True
        for clause in clauses:
            if not any((lit > 0 and assignments.get(lit, False)) or (lit < 0 and not assignments.get(-lit, True)) for lit in clause):
                satisfied = False
                break
        if satisfied:
            return decisions
        unsatisfied_clauses = [clause for clause in clauses if not any((lit > 0 and assignments.get(lit, False)) or (lit < 0 and not assignments.get(-lit, True)) for lit in clause)]
        if not unsatisfied_clauses:
            return decisions
        clause = random.choice(unsatisfied_clauses)
        lit = random.choice(clause)
        assignments[abs(lit)] = lit > 0
        decisions += 1
    return decisions

def run_trial(seed):
    random.seed(seed)
    n_values = [12, 16, 20, 24, 28, 32, 36, 40]
    alpha_values = [4.5, 5.0, 5.5]
    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for alpha in alpha_values:
            m = int(alpha * n)
            clauses = generate_3cnf(n, m)
            if not is_unsatisfiable(clauses):
                continue
            graph = build_clause_sharing_graph(clauses)
            delta = compute_dismantlability_defect(graph)
            t_star = count_dpll_decisions(clauses)
            if delta == 0:
                continue
            R = 8 * m * math.log2(t_star + 1) / (n * delta)
            metric_values.append(R)
            instances_tested += 1
            if R < 1.0:
                conjecture_holds = False
                counterexample = f"n={n}, alpha={alpha}, R={R}"

    if not metric_values:
        return {
            "metric_name": "min_R",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }

    min_R = min(metric_values)
    if min_R < 1.0:
        conjecture_holds = False
        counterexample = f"min_R={min_R}"

    return {
        "metric_name": "min_R",
        "metric_value": min_R,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    trials = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        trials.append(trial)

    metric_values = [trial["metric_value"] for trial in trials if trial["instances_tested"] > 0]
    if not metric_values:
        print("RESULT: INCONCLUSIVE reason=no_valid_instances")
        sys.exit(0)

    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for trial in trials if trial["conjecture_holds"]) / len(trials)

    if all(trial["conjecture_holds"] for trial in trials):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not trial["conjecture_holds"] for trial in trials):
        first_failing_seed = seeds[next(i for i, trial in enumerate(trials) if not trial["conjecture_holds"])]
        counterexample = trials[next(i for i, trial in enumerate(trials) if not trial["conjecture_holds"])]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")