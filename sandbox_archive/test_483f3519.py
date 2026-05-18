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
            clause[0] *= -1
        if random.random() < 0.5:
            clause[1] *= -1
        if random.random() < 0.5:
            clause[2] *= -1
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
            if all(lit < 0 and -lit not in assignments or lit > 0 and lit not in assignments for lit in clause):
                satisfied = False
                break
        if satisfied:
            return False
        if len(assignments) == n:
            return True
        var = random.choice(range(1, n + 1))
        assignments[var] = random.choice([True, False])
    return True

def build_clause_sharing_graph(clauses):
    graph = defaultdict(set)
    for i, clause1 in enumerate(clauses):
        for j, clause2 in enumerate(clauses):
            if i != j:
                if any(abs(lit1) == abs(lit2) for lit1 in clause1 for lit2 in clause2):
                    graph[i].add(j)
    return graph

def compute_dismantlability_defect(graph):
    graph = {k: set(v) for k, v in graph.items()}
    delta = 0
    while graph:
        dominated = False
        for v in list(graph.keys()):
            neighbors = graph[v].union({v})
            if all(any(w in graph and v in graph[w] for w in neighbors) for w in neighbors):
                del graph[v]
                for u in graph:
                    if v in graph[u]:
                        graph[u].remove(v)
                dominated = True
                break
        if not dominated:
            delta += len(graph)
            break
    return delta

def count_dpll_nodes(clauses, max_nodes=1000000):
    n = max(abs(lit) for clause in clauses for lit in clause)
    assignments = {}
    nodes = 0
    stack = [(assignments.copy(), 0)]
    while stack and nodes < max_nodes:
        current_assignments, depth = stack.pop()
        nodes += 1
        satisfied = True
        for clause in clauses:
            if all(lit < 0 and -lit not in current_assignments or lit > 0 and lit not in current_assignments for lit in clause):
                satisfied = False
                break
        if satisfied:
            continue
        if len(current_assignments) == n:
            return nodes
        var = random.choice(range(1, n + 1))
        if var not in current_assignments:
            new_assignments = current_assignments.copy()
            new_assignments[var] = True
            stack.append((new_assignments, depth + 1))
            new_assignments = current_assignments.copy()
            new_assignments[var] = False
            stack.append((new_assignments, depth + 1))
    return nodes

def run_trial(seed):
    random.seed(seed)
    n_values = [12, 16, 20, 24, 28, 32, 36, 40]
    alpha_values = [4.5, 5.0, 5.5]
    results = []
    for n in n_values:
        for alpha in alpha_values:
            m = int(alpha * n)
            clauses = generate_3cnf(n, m)
            if not is_unsatisfiable(clauses):
                continue
            graph = build_clause_sharing_graph(clauses)
            delta = compute_dismantlability_defect(graph)
            t_star = count_dpll_nodes(clauses)
            if delta == 0:
                delta = 1
            R = 8 * m * math.log2(t_star + 1) / (n * delta)
            results.append({
                "n": n,
                "alpha": alpha,
                "m": m,
                "delta": delta,
                "t_star": t_star,
                "R": R
            })
    if not results:
        return {
            "metric_name": "R",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }
    min_R = min(r["R"] for r in results)
    conjecture_holds = min_R >= 1.0
    counterexample = "" if conjecture_holds else f"R={min_R:.4f} < 1.0"
    return {
        "metric_name": "R",
        "metric_value": min_R,
        "instances_tested": len(results),
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
    metric_values = [t["metric_value"] for t in trials if t["instances_tested"] > 0]
    if not metric_values:
        print("RESULT: INCONCLUSIVE reason=no_valid_instances")
        sys.exit(0)
    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for t in trials if t["conjecture_holds"]) / len(trials)
    if all(t["conjecture_holds"] for t in trials):
        print(f"RESULT: SUPPORTED mean={mean:.4f} std={std:.4f} support_fraction={support_fraction:.4f}")
    elif any(not t["conjecture_holds"] for t in trials):
        first_failing_seed = seeds[next(i for i, t in enumerate(trials) if not t["conjecture_holds"])]
        counterexample = next(t["counterexample"] for t in trials if not t["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")