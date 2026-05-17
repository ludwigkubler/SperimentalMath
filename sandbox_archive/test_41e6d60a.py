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
from collections import deque

def generate_3_regular_graph(n, seed):
    random.seed(seed)
    if n % 2 != 0:
        raise ValueError("n must be even for 3-regular graph")
    stubs = list(range(n)) * 3
    edges = set()
    while stubs:
        u = stubs.pop()
        v = random.choice([x for x in stubs if x != u])
        stubs.remove(v)
        edges.add(frozenset({u, v}))
    return edges

def is_connected(edges, n):
    if not edges:
        return False
    graph = {i: set() for i in range(n)}
    for u, v in edges:
        graph[u].add(v)
        graph[v].add(u)
    visited = set()
    queue = deque([0])
    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.add(node)
            queue.extend(graph[node] - visited)
    return len(visited) == n

def compute_min_vertex_separator(edges, n):
    if not is_connected(edges, n):
        return 0
    min_separator = float('inf')
    for k in range(1, n):
        for subset in itertools.combinations(range(n), k):
            A = set(subset)
            S = set()
            for u in A:
                for v in range(n):
                    if v not in A and v not in S:
                        if v in [x for x in range(n) if any((u, x) in edges or (x, u) in edges)]:
                            S.add(v)
            if len(A) >= n // 3 and len(set(range(n)) - A - S) >= n // 3:
                min_separator = min(min_separator, len(S))
    return min_separator if min_separator != float('inf') else 0

def compute_nu_30(edges, n):
    k = n // 2
    nu_values = []
    for _ in range(30):
        U = random.sample(range(n), k)
        subgraph_edges = [edge for edge in edges if edge.issubset(U)]
        nu_values.append(compute_min_vertex_separator(subgraph_edges, k))
    return sum(nu_values) / len(nu_values)

def generate_tseitin_cnf(edges, n, seed):
    random.seed(seed)
    omega = [random.choice([-1, 1]) for _ in range(n)]
    clauses = []
    for u, v in edges:
        x = f"x_{u}_{v}"
        clauses.append([x, f"v_{u}", f"v_{v}"])
        clauses.append([f"-{x}", f"v_{u}", f"-v_{v}"])
        clauses.append([f"-{x}", f"-v_{u}", f"v_{v}"])
        clauses.append([x, f"-v_{u}", f"-v_{v}"])
    for i in range(n):
        if omega[i] == 1:
            clauses.append([f"v_{i}"])
        else:
            clauses.append([f"-v_{i}"])
    return clauses

def dpll_satisfiable(clauses, max_nodes=10**6):
    assignments = {}
    nodes = 0

    def unit_propagate():
        nonlocal nodes
        changed = True
        while changed:
            changed = False
            for clause in clauses:
                unassigned = [lit for lit in clause if lit not in assignments]
                if len(unassigned) == 1:
                    lit = unassigned[0]
                    if lit.startswith('-'):
                        assignments[lit[1:]] = False
                    else:
                        assignments[lit] = True
                    changed = True
                    nodes += 1
                    if nodes > max_nodes:
                        return False
        return True

    def dpll():
        nonlocal nodes
        if not unit_propagate():
            return False, nodes
        for clause in clauses:
            if all(lit in assignments and (lit.startswith('-') != assignments.get(lit[1:], None)) for lit in clause):
                return False, nodes
        if all(lit in assignments for clause in clauses for lit in clause):
            return True, nodes
        for clause in clauses:
            for lit in clause:
                if lit not in assignments:
                    if lit.startswith('-'):
                        var = lit[1:]
                    else:
                        var = lit
                    if var not in assignments:
                        assignments[var] = True
                        satisfied, nodes = dpll()
                        if satisfied:
                            return True, nodes
                        assignments[var] = False
                        satisfied, nodes = dpll()
                        if satisfied:
                            return True, nodes
                        del assignments[var]
                        return False, nodes
        return False, nodes

    satisfied, nodes = dpll()
    return math.log2(nodes) if satisfied else float('inf')

def run_trial(seed):
    n_values = [8, 10, 12, 14, 16, 18, 20]
    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        try:
            edges = generate_3_regular_graph(n, seed)
            if not is_connected(edges, n):
                continue
            nu_30 = compute_nu_30(edges, n)
            cnf = generate_tseitin_cnf(edges, n, seed)
            log2_s = dpll_satisfiable(cnf)
            metric_values.append(log2_s)
            instances_tested += 1

            if log2_s < 0.1 * nu_30:
                conjecture_holds = False
                counterexample = f"Instance with n={n}, log2(s*)={log2_s}, nu_30={nu_30}"
                break
        except IndexError:
            continue

    if conjecture_holds:
        for n in [8, 12, 16, 20]:
            try:
                edges = generate_3_regular_graph(n, seed)
                if not is_connected(edges, n):
                    continue
                nu_30 = compute_nu_30(edges, n)
                if nu_30 > 2:
                    conjecture_holds = False
                    counterexample = f"Anchor instance with n={n}, nu_30={nu_30}"
                    break
            except IndexError:
                continue

    return {
        "metric_name": "log2(s*)",
        "metric_value": sum(metric_values) / len(metric_values) if metric_values else 0,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        result["seed"] = seed
        print(f"TRIAL: {result}")
        results.append(result)

    metric_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    if metric_values:
        mean = sum(metric_values) / len(metric_values)
        std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    else:
        mean, std = 0, 0

    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")