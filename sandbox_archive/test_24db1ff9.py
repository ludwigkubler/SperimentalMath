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
    for _ in range(m):
        clause = random.sample(variables, 3)
        if random.random() < 0.5:
            clause[0] = -clause[0]
        if random.random() < 0.5:
            clause[1] = -clause[1]
        if random.random() < 0.5:
            clause[2] = -clause[2]
        clauses.append(clause)
    # Ensure unsatisfiability by adding a forced clause
    forced_clause = [random.choice(variables), -random.choice(variables), random.choice(variables)]
    clauses.append(forced_clause)
    return clauses

def build_clause_sharing_graph(clauses):
    graph = defaultdict(set)
    for i, clause1 in enumerate(clauses):
        for j, clause2 in enumerate(clauses):
            if i != j:
                vars1 = set(abs(lit) for lit in clause1)
                vars2 = set(abs(lit) for lit in clause2)
                if vars1 & vars2:
                    graph[i].add(j)
    return graph

def compute_dismantlability_defect(graph):
    graph = {k: set(v) for k, v in graph.items()}
    delta = 0
    while graph:
        dominated = False
        for v in list(graph.keys()):
            neighbors = graph[v]
            if all(any(u in graph[v] for u in graph[w]) for w in neighbors):
                del graph[v]
                for u in graph:
                    if v in graph[u]:
                        graph[u].remove(v)
                dominated = True
                break
        if not dominated:
            delta += 1
            graph.popitem()
    return delta

def dpll(clauses, assignments, decision_nodes):
    decision_nodes[0] += 1
    if not clauses:
        return True
    for clause in clauses:
        if all(lit in assignments or -lit in assignments for lit in clause):
            continue
        if all(lit in assignments or -lit not in assignments for lit in clause):
            return False
    for clause in clauses:
        unassigned = [lit for lit in clause if lit not in assignments and -lit not in assignments]
        if len(unassigned) == 1:
            lit = unassigned[0]
            new_assignments = assignments.copy()
            new_assignments.add(lit)
            if dpll(clauses, new_assignments, decision_nodes):
                return True
    for clause in clauses:
        unassigned = [lit for lit in clause if lit not in assignments and -lit not in assignments]
        if unassigned:
            lit = unassigned[0]
            new_assignments = assignments.copy()
            new_assignments.add(lit)
            if dpll(clauses, new_assignments, decision_nodes):
                return True
            new_assignments = assignments.copy()
            new_assignments.add(-lit)
            if dpll(clauses, new_assignments, decision_nodes):
                return True
            return False
    return False

def measure_t_star(clauses):
    decision_nodes = [0]
    dpll(clauses, set(), decision_nodes)
    return decision_nodes[0]

def run_trial(seed):
    n_values = [12, 16, 20, 24, 28, 32, 36, 40]
    alpha_values = [4.5, 5.0, 5.5]
    results = []
    for n in n_values:
        for alpha in alpha_values:
            clauses = generate_unsat_3cnf(n, alpha, seed)
            graph = build_clause_sharing_graph(clauses)
            delta = compute_dismantlability_defect(graph)
            t_star = measure_t_star(clauses)
            m = len(clauses)
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
    min_R = min(r["R"] for r in results)
    delta_m = [r["delta"] / r["m"] for r in results]
    log_t_star_n = [math.log2(r["t_star"]) / r["n"] for r in results]
    rho = spearman_rho(delta_m, log_t_star_n)
    conjecture_holds = min_R >= 1.0 and rho >= 0.4
    counterexample = "" if conjecture_holds else f"R(F) = {min_R:.3f} < 1.0"
    return {
        "metric_name": "min_R",
        "metric_value": min_R,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def spearman_rho(x, y):
    n = len(x)
    rank_x = rank(x)
    rank_y = rank(y)
    d = sum((rx - ry) ** 2 for rx, ry in zip(rank_x, rank_y))
    return 1 - (6 * d) / (n * (n ** 2 - 1))

def rank(values):
    sorted_values = sorted((v, i) for i, v in enumerate(values))
    ranks = [0] * len(values)
    for rank, (value, original_index) in enumerate(sorted_values):
        ranks[original_index] = rank + 1
    return ranks

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    trials = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        trials.append(trial)
    metric_values = [t["metric_value"] for t in trials]
    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(t["conjecture_holds"] for t in trials) / len(trials)
    if all(t["conjecture_holds"] for t in trials):
        print(f"RESULT: SUPPORTED mean={mean:.3f} std={std:.3f} support_fraction={support_fraction:.3f}")
    elif any(not t["conjecture_holds"] for t in trials):
        first_failing_seed = seeds[next(i for i, t in enumerate(trials) if not t["conjecture_holds"])]
        counterexample = next(t["counterexample"] for t in trials if not t["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=all_trials_failed")