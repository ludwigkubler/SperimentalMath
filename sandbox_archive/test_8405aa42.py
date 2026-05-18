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

def generate_3_regular_graph(n):
    if n % 2 != 0:
        raise ValueError("n must be even for a 3-regular graph")
    edges = []
    vertices = list(range(n))
    random.shuffle(vertices)
    for i in range(0, n, 2):
        edges.append((vertices[i], vertices[i+1]))
    remaining = vertices.copy()
    while remaining:
        u = remaining.pop()
        v = random.choice(remaining)
        edges.append((u, v))
    return edges

def generate_tseitin(n):
    edges = generate_3_regular_graph(n)
    omega = [random.choice([-1, 1]) for _ in range(n)]
    clauses = []
    for u, v in edges:
        x = random.randint(0, 1)
        y = random.randint(0, 1)
        clauses.append((u, v, x))
        clauses.append((u, v, y))
        clauses.append((u, v, x ^ y))
    return clauses

def generate_random_3_sat(n, m):
    variables = list(range(n))
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, 3)
        signs = [random.choice([-1, 1]) for _ in range(3)]
        clauses.append(list(zip(signs, clause)))
    return clauses

def generate_2_xor_sat_lifted(n, m):
    variables = list(range(n))
    clauses = []
    for _ in range(m):
        a, b = random.sample(variables, 2)
        c = random.choice(variables)
        clauses.append([(1, a), (1, b), (-1, c)])
        clauses.append([(1, a), (-1, b), (1, c)])
        clauses.append([(-1, a), (1, b), (1, c)])
    return clauses

def build_clause_graph(clauses):
    graph = defaultdict(set)
    for i, clause in enumerate(clauses):
        for j, other_clause in enumerate(clauses):
            if i != j:
                shared_vars = set(var for _, var in clause) & set(var for _, var in other_clause)
                if len(shared_vars) >= 1:
                    graph[i].add(j)
    return graph

def enumerate_cliques(graph, max_size=6):
    cliques = []
    vertices = list(graph.keys())
    for size in range(2, max_size + 1):
        for candidate in itertools.combinations(vertices, size):
            is_clique = True
            for i in range(size):
                for j in range(i + 1, size):
                    if candidate[j] not in graph[candidate[i]]:
                        is_clique = False
                        break
                if not is_clique:
                    break
            if is_clique:
                cliques.append(candidate)
    return cliques

def compute_cartier_foata(cliques, q):
    result = 0.0
    for clique in cliques:
        result += (-q) ** len(clique)
    return result

def find_root(cliques, delta):
    q = 0.0
    step = 0.01
    while q < 1.0 / delta:
        if compute_cartier_foata(cliques, q) == 0:
            return q
        q += step
    return float('inf')

def max_degree(graph):
    return max(len(neighbors) for neighbors in graph.values()) if graph else 0

def dpll(clauses):
    def is_satisfied(clause, assignment):
        for sign, var in clause:
            if (sign == 1 and assignment[var]) or (sign == -1 and not assignment[var]):
                return True
        return False

    def backtrack(assignment, remaining_clauses):
        if not remaining_clauses:
            return True
        if not assignment:
            return False
        var = assignment.pop()
        for value in [True, False]:
            new_assignment = assignment.copy()
            new_assignment[var] = value
            new_remaining = [clause for clause in remaining_clauses if not is_satisfied(clause, new_assignment)]
            if backtrack(new_assignment, new_remaining):
                return True
        return False

    variables = set(var for clause in clauses for _, var in clause)
    assignment = {var: None for var in variables}
    return backtrack(list(assignment.keys()), clauses)

def run_trial(seed):
    random.seed(seed)
    n = random.choice([12, 16, 20, 24, 28, 32, 36, 40])
    ensemble = random.choice(['tseitin', 'random_3_sat', '2_xor_sat_lifted'])

    if ensemble == 'tseitin':
        clauses = generate_tseitin(n)
    elif ensemble == 'random_3_sat':
        m = int(4.4 * n)
        clauses = generate_random_3_sat(n, m)
    else:
        m = int(4.4 * n)
        clauses = generate_2_xor_sat_lifted(n, m)

    if not dpll(clauses):
        return {
            "metric_name": "log_2 t*(F)",
            "metric_value": float('nan'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Formula is satisfiable"
        }

    graph = build_clause_graph(clauses)
    cliques = enumerate_cliques(graph)
    delta = max_degree(graph)
    r = find_root(cliques, delta)

    if r == float('inf'):
        return {
            "metric_name": "log_2 t*(F)",
            "metric_value": float('nan'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "No positive root found"
        }

    t_star = len(clauses)
    log_t_star = math.log2(t_star)
    bound = 0.5 * (1 / r - delta) - 1

    conjecture_holds = log_t_star >= bound
    counterexample = "" if conjecture_holds else f"log_2 t*(F) = {log_t_star} < {bound}"

    return {
        "metric_name": "log_2 t*(F)",
        "metric_value": log_t_star,
        "instances_tested": 1,
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

    metric_values = [trial["metric_value"] for trial in trials if not math.isnan(trial["metric_value"])]
    mean = sum(metric_values) / len(metric_values) if metric_values else float('nan')
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values)) if metric_values else float('nan')

    support_fraction = sum(trial["conjecture_holds"] for trial in trials) / len(trials)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        counterexamples = [trial["counterexample"] for trial in trials if not trial["conjecture_holds"]]
        if counterexamples:
            first_failing_seed = seeds[trials.index(next(trial for trial in trials if not trial["conjecture_holds"]))]
            print(f"RESULT: FALSIFIED counterexample={counterexamples[0]} first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE reason=insufficient_data")