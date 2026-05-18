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

def generate_tseitin(n):
    if n % 2 != 0:
        n += 1
    G = [set() for _ in range(n)]
    for i in range(n):
        neighbors = [j for j in range(n) if j != i]
        random.shuffle(neighbors)
        for j in neighbors[:3]:
            G[i].add(j)
            G[j].add(i)
    omega = [random.choice([-1, 1]) for _ in range(n)]
    formula = []
    for i in range(n):
        for j in G[i]:
            if i < j:
                x = i + 1
                y = j + 1
                z = n + 1 + (i * n + j) // 2
                formula.append([x, y, -z])
                formula.append([-x, -y, -z])
                formula.append([x, -y, z])
                formula.append([-x, y, z])
    for i in range(n):
        if omega[i] == 1:
            formula.append([i + 1])
        else:
            formula.append([-(i + 1)])
    return formula

def generate_random_3sat(n, m):
    variables = list(range(1, n + 1))
    formula = []
    for _ in range(m):
        clause = random.sample(variables, 3)
        for i in range(3):
            if random.random() < 0.5:
                clause[i] = -clause[i]
        formula.append(clause)
    return formula

def generate_2xor_lifted(n, m):
    variables = list(range(1, n + 1))
    formula = []
    for _ in range(m):
        x, y = random.sample(variables, 2)
        z = random.randint(1, n)
        formula.append([x, y, -z])
        formula.append([x, -y, z])
        formula.append([-x, y, z])
        formula.append([-x, -y, -z])
    return formula

def is_unsatisfiable(formula):
    n = max(max(abs(lit) for lit in clause) for clause in formula) + 1
    assignments = [None] * n
    stack = []
    for clause in formula:
        satisfied = False
        for lit in clause:
            if assignments[abs(lit) - 1] is not None:
                if (lit > 0 and assignments[abs(lit) - 1]) or (lit < 0 and not assignments[abs(lit) - 1]):
                    satisfied = True
                    break
        if not satisfied:
            stack.append(clause)
    while stack:
        clause = stack.pop()
        for lit in clause:
            var = abs(lit)
            if assignments[var - 1] is None:
                assignments[var - 1] = lit > 0
                for other_clause in formula:
                    if clause != other_clause:
                        satisfied = False
                        for other_lit in other_clause:
                            if assignments[abs(other_lit) - 1] is not None:
                                if (other_lit > 0 and assignments[abs(other_lit) - 1]) or (other_lit < 0 and not assignments[abs(other_lit) - 1]):
                                    satisfied = True
                                    break
                        if not satisfied:
                            stack.append(other_clause)
                break
    return any(all(assignments[abs(lit) - 1] is not None and ((lit > 0 and assignments[abs(lit) - 1]) or (lit < 0 and not assignments[abs(lit) - 1])) for lit in clause) for clause in formula)

def build_graph(formula):
    n = max(max(abs(lit) for lit in clause) for clause in formula) + 1
    graph = defaultdict(set)
    for i, clause1 in enumerate(formula):
        for j, clause2 in enumerate(formula):
            if i < j:
                shared_vars = set(abs(lit) for lit in clause1) & set(abs(lit) for lit in clause2)
                if shared_vars:
                    graph[i].add(j)
                    graph[j].add(i)
    return graph

def find_cliques(graph, max_size):
    cliques = []
    for size in range(2, max_size + 1):
        for nodes in itertools.combinations(graph.keys(), size):
            if all(j in graph[i] for i in nodes for j in nodes if i != j):
                cliques.append(nodes)
    return cliques

def compute_cartier_foata(cliques, q):
    result = 0
    for clique in cliques:
        result += (-q) ** len(clique)
    return result

def find_root(coeffs):
    if not coeffs:
        return float('inf')
    for q in [0.1 * i for i in range(1, 101)]:
        if compute_cartier_foata(coeffs, q) == 0:
            return q
    return float('inf')

def compute_max_degree(graph):
    if not graph:
        return 0
    return max(len(neighbors) for neighbors in graph.values())

def run_dpll(formula):
    n = max(max(abs(lit) for lit in clause) for clause in formula) + 1
    assignments = [None] * n
    stack = []
    for clause in formula:
        satisfied = False
        for lit in clause:
            if assignments[abs(lit) - 1] is not None:
                if (lit > 0 and assignments[abs(lit) - 1]) or (lit < 0 and not assignments[abs(lit) - 1]):
                    satisfied = True
                    break
        if not satisfied:
            stack.append(clause)
    while stack:
        clause = stack.pop()
        for lit in clause:
            var = abs(lit)
            if assignments[var - 1] is None:
                assignments[var - 1] = lit > 0
                for other_clause in formula:
                    if clause != other_clause:
                        satisfied = False
                        for other_lit in other_clause:
                            if assignments[abs(other_lit) - 1] is not None:
                                if (other_lit > 0 and assignments[abs(other_lit) - 1]) or (other_lit < 0 and not assignments[abs(other_lit) - 1]):
                                    satisfied = True
                                    break
                        if not satisfied:
                            stack.append(other_clause)
                break
    return sum(1 for a in assignments if a is not None)

def run_trial(seed):
    random.seed(seed)
    n = random.choice([12, 16, 20, 24, 28, 32, 36, 40])
    ensemble = random.choice(['tseitin', 'random_3sat', '2xor_lifted'])
    if ensemble == 'tseitin':
        formula = generate_tseitin(n)
    elif ensemble == 'random_3sat':
        m = int(4.4 * n)
        formula = generate_random_3sat(n, m)
    else:
        m = int(4.4 * n)
        formula = generate_2xor_lifted(n, m)
    if not is_unsatisfiable(formula):
        return {
            "metric_name": "log2_tstar",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }
    graph = build_graph(formula)
    cliques = find_cliques(graph, 6)
    r = find_root(cliques)
    delta = compute_max_degree(graph)
    tstar = run_dpll(formula)
    log2_tstar = math.log2(tstar) if tstar > 0 else 0
    metric_value = log2_tstar
    conjecture_holds = log2_tstar >= 0.5 * (1 / r - delta) - 1 if r > 0 else True
    counterexample = f"log2_tstar={log2_tstar}, r={r}, delta={delta}" if not conjecture_holds else ""
    return {
        "metric_name": "log2_tstar",
        "metric_value": metric_value,
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
    metric_values = [trial["metric_value"] for trial in trials]
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
        print("RESULT: INCONCLUSIVE reason=unknown")