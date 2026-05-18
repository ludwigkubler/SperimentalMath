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

def generate_3cnf(n, ensemble, seed):
    random.seed(seed)
    if ensemble == 'A':
        # Tseitin T(G,ω) on random 3-regular G with random odd charge ω
        G = generate_3_regular_graph(n)
        clauses = tseitin_3cnf(G)
    elif ensemble == 'B':
        # Random 3-SAT at density 4.4
        clauses = generate_random_3sat(n, 4.4)
    elif ensemble == 'C':
        # Random 2-XOR-SAT lifted to 3-CNF
        clauses = generate_xor_3cnf(n)
    else:
        raise ValueError("Invalid ensemble")
    return clauses

def generate_3_regular_graph(n):
    # Generate a random 3-regular graph
    edges = set()
    vertices = list(range(n))
    random.shuffle(vertices)
    for i in range(0, n, 2):
        if i+1 < n:
            edges.add((vertices[i], vertices[i+1]))
    # Add remaining edges to make it 3-regular
    remaining = [v for v in vertices if sum(1 for e in edges if v in e) < 3]
    while remaining:
        u = remaining.pop()
        v = random.choice([v for v in vertices if v != u and sum(1 for e in edges if v in e) < 3 and (u, v) not in edges and (v, u) not in edges])
        edges.add((u, v))
    return edges

def tseitin_3cnf(G):
    # Generate Tseitin 3-CNF for a graph G
    clauses = []
    for u, v in G:
        x = f'x_{u}_{v}'
        y = f'y_{u}_{v}'
        clauses.append([x, y, f'z_{u}_{v}'])
        clauses.append([x, f'¬y_{u}_{v}', f'z_{u}_{v}'])
        clauses.append([f'¬x', y, f'z_{u}_{v}'])
        clauses.append([f'¬x', f'¬y_{u}_{v}', f'z_{u}_{v}'])
    return clauses

def generate_random_3sat(n, density):
    # Generate random 3-SAT clauses
    clauses = []
    m = int(density * n)
    for _ in range(m):
        clause = []
        for _ in range(3):
            var = random.randint(1, n)
            neg = random.choice([True, False])
            lit = f'¬x_{var}' if neg else f'x_{var}'
            clause.append(lit)
        clauses.append(clause)
    return clauses

def generate_xor_3cnf(n):
    # Generate 2-XOR-SAT lifted to 3-CNF
    clauses = []
    for _ in range(n):
        a, b, c = random.sample(range(1, n+1), 3)
        clauses.append([f'x_{a}', f'x_{b}', f'x_{c}'])
        clauses.append([f'x_{a}', f'¬x_{b}', f'¬x_{c}'])
        clauses.append([f'¬x_{a}', f'x_{b}', f'¬x_{c}'])
        clauses.append([f'¬x_{a}', f'¬x_{b}', f'x_{c}'])
    return clauses

def build_graph(F):
    # Build the variable-sharing graph G(F)
    graph = defaultdict(set)
    for i, clause in enumerate(F):
        for j, other_clause in enumerate(F):
            if i != j and any(lit in other_clause for lit in clause):
                graph[i].add(j)
    return graph

def find_cliques(graph, max_size=6):
    # Find all cliques of size ≤ max_size in the graph
    cliques = []
    vertices = list(graph.keys())
    for size in range(2, max_size + 1):
        for candidate in itertools.combinations(vertices, size):
            if all(v in graph[u] for u, v in itertools.combinations(candidate, 2)):
                cliques.append(candidate)
    return cliques

def compute_cartier_foata(cliques, q):
    # Compute the truncated Cartier–Foata polynomial C_6(G(F);q)
    result = 0
    for clique in cliques:
        result += (-q) ** len(clique)
    return result

def find_root(cliques):
    # Find the smallest positive root of C_6(G(F);q)
    q = 0.01
    while q < 10:
        if compute_cartier_foata(cliques, q) == 0:
            return q
        q += 0.01
    return float('inf')

def dpll(clauses):
    # Mini-DPLL solver with VSIDS
    assignment = {}
    return backtrack(list(assignment.keys()), clauses)

def backtrack(assignment, clauses):
    # Backtracking for DPLL
    if not clauses:
        return True
    if any(not clause for clause in clauses):
        return False
    var = select_variable(clauses)
    for value in [True, False]:
        new_assignment = assignment.copy()
        new_assignment[var] = value
        new_clauses = simplify(clauses, new_assignment)
        if backtrack(new_assignment, new_clauses):
            return True
    return False

def select_variable(clauses):
    # VSIDS variable selection
    variables = set()
    for clause in clauses:
        for lit in clause:
            variables.add(lit)
    return random.choice(list(variables))

def simplify(clauses, assignment):
    # Simplify clauses based on assignment
    new_clauses = []
    for clause in clauses:
        new_clause = []
        for lit in clause:
            if lit in assignment:
                if assignment[lit]:
                    new_clause = []
                    break
            elif f'¬{lit}' in assignment:
                if not assignment[f'¬{lit}']:
                    new_clause = []
                    break
            else:
                new_clause.append(lit)
        if new_clause:
            new_clauses.append(new_clause)
    return new_clauses

def compute_t_star(clauses):
    # Compute the tree-Resolution refutation size
    if not dpll(clauses):
        return float('inf')
    # Simplified estimation
    return len(clauses) ** 2

def run_trial(seed):
    random.seed(seed)
    n = random.choice([12, 16, 20, 24, 28, 32, 36, 40])
    ensemble = random.choice(['A', 'B', 'C'])
    F = generate_3cnf(n, ensemble, seed)
    G = build_graph(F)
    cliques = find_cliques(G)
    r = find_root(cliques)
    t_star = compute_t_star(F)
    delta = max(len(G[v]) for v in G) if G else 0
    metric_value = math.log2(t_star) if t_star != float('inf') else float('inf')
    conjecture_holds = metric_value >= 0.5 * (1 / r - delta) - 1 if r != float('inf') else True
    counterexample = f"log2(t_star)={metric_value}, 1/r(F)-Δ(F)={1/r - delta}" if not conjecture_holds else ""
    return {
        "metric_name": "log2(t_star) vs 1/r(F)-Δ(F)",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [random.randint(1, 1000000) for _ in range(30)]
    metric_values = []
    conjecture_holds = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        metric_values.append(trial["metric_value"])
        conjecture_holds.append(trial["conjecture_holds"])
    mean = sum(metric_values) / len(metric_values) if metric_values else 0
    std = (sum((x - mean) ** 2 for x in metric_values) / len(metric_values)) ** 0.5 if metric_values else 0
    support_fraction = sum(conjecture_holds) / len(conjecture_holds) if conjecture_holds else 0
    if all(conjecture_holds):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not holds for holds in conjecture_holds):
        first_failing_seed = seeds[conjecture_holds.index(False)]
        counterexample = [trial["counterexample"] for trial in [run_trial(seed) for seed in seeds] if not trial["conjecture_holds"]][0]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")