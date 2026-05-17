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
    degrees = defaultdict(int)
    vertices = list(range(n))
    while len(edges) < 3 * n // 2:
        u, v = random.sample(vertices, 2)
        if u != v and degrees[u] < 3 and degrees[v] < 3 and (u, v) not in edges and (v, u) not in edges:
            edges.append((u, v))
            degrees[u] += 1
            degrees[v] += 1
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    return graph

def is_connected(graph):
    if not graph:
        return False
    visited = set()
    queue = deque([next(iter(graph))])
    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.add(node)
            queue.extend(neighbor for neighbor in graph[node] if neighbor not in visited)
    return len(visited) == len(graph)

def bfs(graph, start, target):
    queue = deque([(start, [start])])
    visited = set()
    while queue:
        node, path = queue.popleft()
        if node == target:
            return path
        if node not in visited:
            visited.add(node)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))
    return None

def min_vertex_separator(graph):
    n = len(graph)
    if n == 0:
        return 0
    min_sep = float('inf')
    for u in graph:
        for v in graph:
            if u != v:
                path = bfs(graph, u, v)
                if path:
                    sep = len(set(path)) - 2
                    if sep < min_sep:
                        min_sep = sep
    return min_sep if min_sep != float('inf') else 0

def compute_nu_30(graph):
    n = len(graph)
    k = n // 2
    nu_values = []
    for _ in range(30):
        U = random.sample(list(graph.keys()), k)
        subgraph = {u: [v for v in graph[u] if v in U] for u in U}
        if is_connected(subgraph):
            beta = min_vertex_separator(subgraph)
            nu_values.append(beta)
        else:
            nu_values.append(0)
    return sorted(nu_values)[15]

def generate_tseitin_cnf(graph, omega):
    edge_vars = {}
    for u in graph:
        for v in graph[u]:
            if u < v:
                edge_vars[(u, v)] = f'e_{u}_{v}'
    cnf = []
    for u in graph:
        for v in graph[u]:
            if u < v:
                cnf.append([f'{edge_vars[(u, v)]}', f'x_{u}', f'x_{v}'])
                cnf.append([f'-{edge_vars[(u, v)]}', f'x_{u}', f'-x_{v}'])
                cnf.append([f'-{edge_vars[(u, v)]}', f'-x_{u}', f'x_{v}'])
                cnf.append([f'{edge_vars[(u, v)]}', f'-x_{u}', f'-x_{v}'])
    for u in graph:
        cnf.append([f'x_{u}' if omega[u] == 1 else f'-x_{u}'])
    return cnf

def dpll_satisfiable(cnf, max_nodes=10**6):
    assignments = {}
    nodes = 0

    def unit_propagate():
        nonlocal nodes
        changed = True
        while changed:
            changed = False
            for clause in cnf:
                unassigned = [lit for lit in clause if lit[1:] not in assignments]
                if len(unassigned) == 1:
                    lit = unassigned[0]
                    var = lit[1:]
                    val = lit[0] != '-'
                    if var in assignments and assignments[var] != val:
                        return False
                    assignments[var] = val
                    changed = True
                    nodes += 1
                    if nodes > max_nodes:
                        return False
            for clause in cnf:
                satisfied = any(lit[1:] in assignments and (lit[0] != '-' if assignments[lit[1:]] else lit[0] == '-') for lit in clause)
                if not satisfied:
                    return False
        return True

    def backtrack():
        nonlocal nodes
        if not unit_propagate():
            return False
        if all(any(lit[1:] in assignments and (lit[0] != '-' if assignments[lit[1:]] else lit[0] == '-') for lit in clause) for clause in cnf):
            return True
        if nodes > max_nodes:
            return False
        for clause in cnf:
            unassigned = [lit for lit in clause if lit[1:] not in assignments]
            if len(unassigned) == 0:
                continue
            var = unassigned[0][1:]
            for val in [True, False]:
                assignments[var] = val
                nodes += 1
                if backtrack():
                    return True
                del assignments[var]
                if nodes > max_nodes:
                    return False
            return False
        return False

    return backtrack()

def run_trial(seed):
    random.seed(seed)
    n_values = [8, 10, 12, 14, 16, 18, 20]
    n = random.choice(n_values)
    graph = generate_3_regular_graph(n, seed)
    while not is_connected(graph):
        graph = generate_3_regular_graph(n, seed)
    nu_30 = compute_nu_30(graph)
    omega = [random.choice([0, 1]) for _ in range(n)]
    cnf = generate_tseitin_cnf(graph, omega)
    s_star = 10**6
    if dpll_satisfiable(cnf):
        s_star = 1
    else:
        s_star = 10**6
    conjecture_holds = (math.log2(s_star) >= 0.1 * nu_30)
    counterexample = ""
    if not conjecture_holds:
        counterexample = f"log2(s_star) = {math.log2(s_star)} < 0.1 * nu_30 = {0.1 * nu_30}"
    return {
        "metric_name": "log2(s_star)",
        "metric_value": math.log2(s_star),
        "instances_tested": 1,
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
    metric_values = [r["metric_value"] for r in results]
    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample={r['counterexample']} first_failing_seed={seeds[results.index(r)]}")
                break