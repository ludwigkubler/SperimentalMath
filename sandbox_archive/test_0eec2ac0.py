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
from collections import defaultdict, deque

def generate_3_regular_graph(n, seed):
    random.seed(seed)
    if n % 2 != 0:
        return None
    edges = []
    stubs = list(range(n)) * 3
    while stubs:
        u = random.choice(stubs)
        stubs.remove(u)
        v = random.choice([x for x in stubs if x != u])
        stubs.remove(v)
        edges.append((u, v))
    adj = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    visited = set()
    stack = [0]
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            stack.extend(adj[node])
    if len(visited) != n:
        return None
    return adj

def compute_t_join_partition(adj, omega):
    T = [v for v in adj if omega[v] == 1]
    if len(T) % 2 != 0:
        T.append(min(v for v in adj if v not in T))
    pairs = []
    while T:
        u = T.pop()
        min_dist = float('inf')
        v = None
        for candidate in T:
            dist = bfs_distance(adj, u, candidate)
            if dist < min_dist or (dist == min_dist and candidate < v):
                min_dist = dist
                v = candidate
        if v is not None:
            T.remove(v)
            pairs.append((u, v))
    path_lengths = []
    for u, v in pairs:
        path_lengths.append(bfs_distance(adj, u, v))
    return path_lengths

def bfs_distance(adj, start, end):
    if start == end:
        return 0
    visited = {start: 0}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for neighbor in adj[node]:
            if neighbor not in visited:
                visited[neighbor] = visited[node] + 1
                if neighbor == end:
                    return visited[neighbor]
                queue.append(neighbor)
    return float('inf')

def hook_length_dimension(partition):
    if not partition:
        return 0
    n = sum(partition)
    m = len(partition)
    if m == 0:
        return 0
    log_dim = 0
    for i, part in enumerate(partition):
        for j in range(1, part + 1):
            hook = part - j + (m - i)
            log_dim += math.log2(j) - math.log2(hook)
    return log_dim

def compute_resolution_size(adj, omega, max_nodes=2**18):
    n = len(adj)
    clauses = []
    for v in adj:
        neighbors = adj[v]
        clause = []
        for u in neighbors:
            clause.append((u, v))
        clauses.append(clause)
    for v in adj:
        if omega[v] == 1:
            clauses.append([(v, v)])
    num_vars = n
    num_clauses = len(clauses)
    if num_clauses == 0:
        return 1
    nodes_explored = 0
    queue = deque()
    queue.append(([], []))
    while queue and nodes_explored < max_nodes:
        assignment, unit_clauses = queue.popleft()
        nodes_explored += 1
        satisfied = [False] * num_clauses
        for i, clause in enumerate(clauses):
            for lit in clause:
                if lit in assignment or (-lit[0], -lit[1]) in assignment:
                    satisfied[i] = True
                    break
        if all(satisfied):
            return nodes_explored
        for i, clause in enumerate(clauses):
            if not satisfied[i]:
                unsat_lits = [lit for lit in clause if lit not in assignment and (-lit[0], -lit[1]) not in assignment]
                if len(unsat_lits) == 1:
                    new_assignment = assignment + [unsat_lits[0]]
                    new_unit_clauses = unit_clauses + [i]
                    queue.append((new_assignment, new_unit_clauses))
    return max_nodes

def run_trial(seed):
    n_values = [6, 8, 10, 12]
    results = []
    for n in n_values:
        adj = None
        while adj is None:
            adj = generate_3_regular_graph(n, seed)
            seed += 1
        omega = [random.randint(0, 1) for _ in range(n)]
        if sum(omega) % 2 != 1:
            omega[0] = 1 - omega[0]
        partition = compute_t_join_partition(adj, omega)
        rho = hook_length_dimension(partition)
        if rho == 0:
            continue
        t_star = compute_resolution_size(adj, omega)
        if t_star == 0:
            continue
        log_t_star = math.log2(t_star)
        log_n = math.log2(n + 2)
        r = (log_t_star * log_n) / rho
        results.append({
            "n": n,
            "rho": rho,
            "log_t_star": log_t_star,
            "log_n": log_n,
            "r": r,
            "conjecture_holds": r >= 0.15,
            "counterexample": "" if r >= 0.15 else f"n={n}, rho={rho}, log_t_star={log_t_star}, log_n={log_n}, r={r}"
        })
    if not results:
        return {
            "metric_name": "r",
            "metric_value": 0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }
    min_r = min(r["r"] for r in results)
    worst_case = min(results, key=lambda x: x["r"])
    return {
        "metric_name": "r",
        "metric_value": min_r,
        "instances_tested": len(results),
        "conjecture_holds": min_r >= 0.15,
        "counterexample": worst_case["counterexample"] if min_r < 0.15 else ""
    }

if __name__ == "__main__":
    seeds = sys.argv[1:] if len(sys.argv) > 1 else [random.randint(1, 1000000) for _ in range(30)]
    seeds = [int(seed) for seed in seeds]
    metric_values = []
    conjecture_holds = []
    counterexamples = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        metric_values.append(trial["metric_value"])
        conjecture_holds.append(trial["conjecture_holds"])
        if trial["counterexample"]:
            counterexamples.append(trial["counterexample"])
    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(conjecture_holds) / len(conjecture_holds)
    if counterexamples:
        print(f"RESULT: FALSIFIED counterexample=\"{counterexamples[0]}\" first_failing_seed={seeds[conjecture_holds.index(False)]}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")