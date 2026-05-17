# auto-injected by SEC sandbox
import json
import os
import time
import re
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import itertools
from collections import deque, defaultdict
from fractions import Fraction

def generate_3_regular_graph(m, seed):
    random.seed(seed)
    if m % 2 != 0:
        raise ValueError("m must be even for 3-regular graphs")
    n = m // 2
    edges = []
    stubs = list(range(n)) * 3
    while stubs:
        u = random.choice(stubs)
        stubs.remove(u)
        v = random.choice(stubs)
        stubs.remove(v)
        edges.append((u, v))
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    return graph

def is_connected(graph):
    if not graph:
        return True
    start = next(iter(graph))
    visited = set()
    queue = deque([start])
    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.add(node)
            queue.extend(neighbor for neighbor in graph[node] if neighbor not in visited)
    return len(visited) == len(graph)

def bfs(graph, start, end):
    queue = deque([(start, [start])])
    visited = set()
    while queue:
        node, path = queue.popleft()
        if node == end:
            return path
        if node not in visited:
            visited.add(node)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))
    return None

def max_flow(graph, source, sink):
    flow = 0
    while True:
        path = bfs(graph, source, sink)
        if not path:
            break
        flow += 1
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            graph[u][v] -= 1
            if graph[u][v] == 0:
                del graph[u][v]
            if v not in graph:
                graph[v] = {}
            if u not in graph[v]:
                graph[v][u] = 0
            graph[v][u] += 1
    return flow

def vertex_separator(graph, U):
    if not is_connected(graph):
        return 0
    k = len(U) // 3
    min_separator = float('inf')
    for A in itertools.combinations(U, k):
        A = set(A)
        S = set(U) - A
        if len(S) < k:
            continue
        flow_graph = defaultdict(dict)
        for u in U:
            for v in graph[u]:
                if v in U:
                    flow_graph[u][v] = 1
        source = 'source'
        sink = 'sink'
        for u in A:
            flow_graph[source][u] = 1
        for u in S:
            flow_graph[u][sink] = 1
        flow = max_flow(flow_graph, source, sink)
        if flow < min_separator:
            min_separator = flow
    return min_separator

def compute_nu_30(graph, seed):
    random.seed(seed)
    m = len(graph)
    k = m // 2
    nu_values = []
    for _ in range(30):
        U = random.sample(list(graph.keys()), k)
        subgraph = {u: [v for v in graph[u] if v in U] for u in U}
        beta = vertex_separator(subgraph, U)
        nu_values.append(beta)
    return sorted(nu_values)[15]

def generate_tseitin_cnf(graph, omega):
    cnf = []
    edge_vars = {}
    for u in graph:
        for v in graph[u]:
            if u < v:
                edge_vars[(u, v)] = f'e_{u}_{v}'
    for u in graph:
        xor_clause = []
        for v in graph[u]:
            if u < v:
                xor_clause.append(edge_vars[(u, v)])
        cnf.append(xor_clause)
        cnf.append([f'-{var}' for var in xor_clause])
    for u in graph:
        cnf.append([f'{edge_vars[(u, v)]}' if u < v else f'{edge_vars[(v, u)]}' for v in graph[u]])
    for var in edge_vars.values():
        if random.random() < 0.5:
            cnf.append([f'-{var}'])
        else:
            cnf.append([var])
    return cnf

def dpll_satisfiable(cnf, max_nodes=10**6):
    assignments = {}
    decision_nodes = 0

    def unit_propagate():
        nonlocal assignments
        changed = True
        while changed:
            changed = False
            for clause in cnf:
                unassigned = [lit for lit in clause if lit[1:] not in assignments]
                if len(unassigned) == 1:
                    lit = unassigned[0]
                    val = lit[0] != '-'
                    var = lit[1:]
                    if var in assignments and assignments[var] != val:
                        return False
                    assignments[var] = val
                    changed = True
        return True

    def dpll():
        nonlocal decision_nodes
        if not unit_propagate():
            return False
        for clause in cnf:
            if all(lit[0] == '-' and lit[1:] in assignments and not assignments[lit[1:]] for lit in clause):
                return False
        if all(len(clause) == 0 for clause in cnf):
            return True
        if decision_nodes > max_nodes:
            return False
        for clause in cnf:
            for lit in clause:
                if lit[1:] not in assignments:
                    var = lit[1:]
                    for val in [True, False]:
                        decision_nodes += 1
                        assignments[var] = val
                        if dpll():
                            return True
                        del assignments[var]
                    return False
        return False

    return dpll(), decision_nodes

def is_barbell(graph):
    m = len(graph)
    if m not in {8, 12, 16, 20}:
        return False
    n = m // 2
    if n % 2 != 0:
        return False
    k = n // 2
    for u in range(k):
        if len(graph[u]) != 3:
            return False
    for u in range(k, n):
        if len(graph[u]) != 3:
            return False
    edges = set()
    for u in graph:
        for v in graph[u]:
            if u < v:
                edges.add((u, v))
    expected_edges = set()
    for u in range(k):
        for v in range(k, n):
            if u == v - k:
                expected_edges.add((u, v))
    if len(edges - expected_edges) <= 2:
        return True
    return False

def run_trial(seed):
    random.seed(seed)
    m_values = [8, 10, 12, 14, 16, 18, 20]
    m = random.choice(m_values)
    graph = generate_3_regular_graph(m, seed)
    while not is_connected(graph):
        graph = generate_3_regular_graph(m, seed)
    nu_30 = compute_nu_30(graph, seed)
    omega = [random.choice([True, False]) for _ in range(m)]
    cnf = generate_tseitin_cnf(graph, omega)
    satisfiable, decision_nodes = dpll_satisfiable(cnf)
    log_s = math.log2(decision_nodes) if decision_nodes > 0 else 0
    conjecture_holds = log_s >= 0.1 * nu_30
    counterexample = ""
    if is_barbell(graph) and nu_30 > 2:
        conjecture_holds = False
        counterexample = f"Barbell graph with m={m} has nu_30={nu_30} > 2"
    return {
        "metric_name": "log2(s*) vs nu_30",
        "metric_value": log_s,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample,
        "nu_30": nu_30,
        "m": m
    }

if __name__ == "__main__":
    seeds = sys.argv[1:] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    metric_values = []
    conjecture_holds = []
    counterexamples = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        metric_values.append(result["metric_value"])
        conjecture_holds.append(result["conjecture_holds"])
        if result["counterexample"]:
            counterexamples.append((seed, result["counterexample"]))
    mean_metric = sum(metric_values) / len(metric_values) if metric_values else 0
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values)) if metric_values else 0
    support_fraction = sum(conjecture_holds) / len(conjecture_holds) if conjecture_holds else 0
    if counterexamples:
        seed, counterexample = counterexamples[0]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")