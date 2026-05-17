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
from collections import deque, defaultdict

def generate_3_regular_graph(n, seed):
    random.seed(seed)
    if n % 2 != 0:
        raise ValueError("n must be even for 3-regular graph")
    edges = []
    stubs = list(range(n)) * 3
    while stubs:
        u = random.choice(stubs)
        stubs.remove(u)
        v = random.choice([x for x in stubs if x != u])
        stubs.remove(v)
        edges.append((u, v))
    # Check if the graph is connected
    adj = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    visited = set()
    queue = deque([0])
    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.add(node)
            queue.extend(adj[node])
    if len(visited) != n:
        return None  # Graph is not connected
    return edges

def is_connected(edges, n):
    adj = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    visited = set()
    queue = deque([0])
    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.add(node)
            queue.extend(adj[node])
    return len(visited) == n

def min_vertex_separator(edges, n, U):
    if not is_connected(edges, n):
        return 0
    # Create a vertex-split graph
    split_graph = defaultdict(list)
    for u, v in edges:
        if u in U and v in U:
            split_graph[u].append(v)
            split_graph[v].append(u)
    # Find all possible source and sink pairs
    k = len(U) // 3
    sources = []
    sinks = []
    for subset in itertools.combinations(U, k):
        sources.append(set(subset))
        sinks.append(set(U) - set(subset))
    # Find the minimum vertex separator
    min_sep = float('inf')
    for source in sources:
        for sink in sinks:
            if len(source) >= k and len(sink) >= k:
                # Use BFS to find the minimum vertex separator
                visited = set()
                queue = deque([(u, 0) for u in source])
                while queue:
                    node, dist = queue.popleft()
                    if node in sink:
                        continue
                    if node not in visited:
                        visited.add(node)
                        for neighbor in split_graph[node]:
                            if neighbor not in visited:
                                queue.append((neighbor, dist + 1))
                if len(visited) == len(U):
                    min_sep = min(min_sep, len(visited) - len(source) - len(sink))
    return min_sep

def compute_nu_30(edges, n, seed):
    random.seed(seed)
    k = n // 2
    nu_values = []
    for _ in range(30):
        U = random.sample(range(n), k)
        beta = min_vertex_separator(edges, n, U)
        nu_values.append(beta)
    nu_values.sort()
    return nu_values[15]  # Median of 30 values

def generate_tseitin_cnf(edges, n, seed):
    random.seed(seed)
    edge_vars = {}
    for i, (u, v) in enumerate(edges):
        edge_vars[(u, v)] = f'e{i}'
    clauses = []
    for u, v in edges:
        x = edge_vars[(u, v)]
        clauses.append([x, f'x{u}', f'x{v}'])
        clauses.append([x, f'x{u}', f'¬x{v}'])
        clauses.append([x, f'¬x{u}', f'x{v}'])
        clauses.append([f'¬x', f'x{u}', f'x{v}'])
    # Add odd charge ω
    for i in range(n):
        if random.random() < 0.5:
            clauses.append([f'x{i}'])
        else:
            clauses.append([f'¬x{i}'])
    return clauses

def dpll(clauses, max_nodes=10**6):
    nodes = 0
    def satisfy(clauses, assignment):
        nonlocal nodes
        nodes += 1
        if nodes > max_nodes:
            return None
        if not clauses:
            return assignment
        # Unit propagation
        unit_clauses = [c for c in clauses if len(c) == 1]
        while unit_clauses:
            literal = unit_clauses[0][0]
            new_assignment = assignment.copy()
            if literal.startswith('¬'):
                new_assignment[literal[1:]] = False
            else:
                new_assignment[literal] = True
            new_clauses = []
            for clause in clauses:
                if literal in clause:
                    continue
                new_clause = [l for l in clause if not (l.startswith('¬') and l[1:] == literal) or (literal.startswith('¬') and l[1:] == l)]
                if not new_clause:
                    return None
                new_clauses.append(new_clause)
            clauses = new_clauses
            unit_clauses = [c for c in clauses if len(c) == 1]
        # Choose a variable to split on
        variables = set()
        for clause in clauses:
            for literal in clause:
                if literal.startswith('¬'):
                    variables.add(literal[1:])
                else:
                    variables.add(literal)
        if not variables:
            return assignment
        var = variables.pop()
        # Try assigning True
        new_assignment = assignment.copy()
        new_assignment[var] = True
        new_clauses = []
        for clause in clauses:
            if var in clause:
                continue
            new_clause = [l for l in clause if not (l.startswith('¬') and l[1:] == var)]
            if not new_clause:
                continue
            new_clauses.append(new_clause)
        result = satisfy(new_clauses, new_assignment)
        if result is not None:
            return result
        # Try assigning False
        new_assignment = assignment.copy()
        new_assignment[var] = False
        new_clauses = []
        for clause in clauses:
            if f'¬{var}' in clause:
                continue
            new_clause = [l for l in clause if not (l == var)]
            if not new_clause:
                continue
            new_clauses.append(new_clause)
        result = satisfy(new_clauses, new_assignment)
        if result is not None:
            return result
        return None
    return satisfy(clauses, {}), nodes

def run_trial(seed):
    n_values = [8, 10, 12, 14, 16, 18, 20]
    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    for n in n_values:
        edges = None
        while edges is None:
            edges = generate_3_regular_graph(n, seed)
            seed += 1
        nu_30 = compute_nu_30(edges, n, seed)
        clauses = generate_tseitin_cnf(edges, n, seed)
        assignment, nodes = dpll(clauses)
        s_star = math.log2(nodes) if nodes > 0 else 0
        metric_values.append(s_star)
        instances_tested += 1
        if s_star < 0.1 * nu_30:
            conjecture_holds = False
            counterexample = f"Instance with n={n}, log2(s*)={s_star}, nu_30={nu_30}"
            break
    # Check anchor class
    anchor_n_values = [8, 12, 16, 20]
    for n in anchor_n_values:
        edges = [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5)]
        if n == 12:
            edges += [(8, 9), (9, 10), (10, 11), (11, 8), (0, 8), (1, 9)]
        elif n == 16:
            edges += [(8, 9), (9, 10), (10, 11), (11, 8), (12, 13), (13, 14), (14, 15), (15, 12), (0, 12), (1, 13)]
        elif n == 20:
            edges += [(8, 9), (9, 10), (10, 11), (11, 8), (12, 13), (13, 14), (14, 15), (15, 12), (16, 17), (17, 18), (18, 19), (19, 16), (0, 16), (1, 17)]
        nu_30 = compute_nu_30(edges, n, seed)
        if nu_30 > 2:
            conjecture_holds = False
            counterexample = f"Anchor instance with n={n}, nu_30={nu_30}"
            break
    return {
        "metric_name": "log2(s*)",
        "metric_value": sum(metric_values) / len(metric_values) if metric_values else 0,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    metric_values = []
    conjecture_holds_counts = 0
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        metric_values.append(result["metric_value"])
        if result["conjecture_holds"]:
            conjecture_holds_counts += 1
    mean = sum(metric_values) / len(metric_values) if metric_values else 0
    std = (sum((x - mean) ** 2 for x in metric_values) / len(metric_values)) ** 0.5 if metric_values else 0
    support_fraction = conjecture_holds_counts / len(seeds) if seeds else 0
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")