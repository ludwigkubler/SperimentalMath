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

def generate_3_regular_graph(n, seed):
    random.seed(seed)
    if n % 2 != 0:
        return None
    degrees = [3] * n
    while True:
        edges = []
        stubs = list(range(n))
        random.shuffle(stubs)
        while stubs:
            u = stubs.pop()
            v = stubs.pop()
            edges.append((u, v))
        adj = defaultdict(list)
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)
        if all(len(adj[u]) == 3 for u in range(n)):
            return adj
    return None

def is_connected(adj, n):
    visited = [False] * n
    stack = [0]
    visited[0] = True
    count = 1
    while stack:
        u = stack.pop()
        for v in adj[u]:
            if not visited[v]:
                visited[v] = True
                stack.append(v)
                count += 1
    return count == n

def generate_charge(n, seed):
    random.seed(seed)
    charge = [random.randint(0, 1) for _ in range(n)]
    if sum(charge) % 2 == 0:
        charge[0] = 1 - charge[0]
    return charge

def greedy_t_join(adj, charge, n):
    T = [u for u in range(n) if charge[u] == 1]
    if len(T) % 2 != 0:
        T.append(min(set(range(n)) - set(T)))
    pairs = []
    while len(T) > 0:
        u = T.pop()
        min_dist = float('inf')
        v = -1
        for candidate in T:
            dist = bfs_distance(adj, u, candidate, n)
            if dist < min_dist or (dist == min_dist and candidate < v):
                min_dist = dist
                v = candidate
        if v != -1:
            pairs.append((u, v))
            T.remove(v)
    path_lengths = []
    for u, v in pairs:
        path_lengths.append(bfs_distance(adj, u, v, n))
    return path_lengths

def bfs_distance(adj, u, v, n):
    if u == v:
        return 0
    visited = [False] * n
    queue = [(u, 0)]
    visited[u] = True
    while queue:
        current, dist = queue.pop(0)
        for neighbor in adj[current]:
            if not visited[neighbor]:
                if neighbor == v:
                    return dist + 1
                visited[neighbor] = True
                queue.append((neighbor, dist + 1))
    return float('inf')

def hook_length_formula(partition):
    if not partition:
        return 1
    n = sum(partition)
    m = len(partition)
    numerator = math.factorial(n)
    denominator = 1
    for part in partition:
        denominator *= math.factorial(part)
    for i in range(1, m + 1):
        denominator *= math.factorial(i)
    for part in partition:
        for j in range(1, part + 1):
            denominator *= j
    return numerator // denominator

def compute_rho(partition):
    if not partition:
        return 0
    dim = hook_length_formula(partition)
    return math.log2(dim) if dim > 0 else 0

def dpll_sat_count(clauses, n):
    def unit_propagate(assignment, clauses):
        changed = True
        while changed:
            changed = False
            for clause in clauses:
                unassigned = [lit for lit in clause if abs(lit) not in assignment]
                if len(unassigned) == 1:
                    lit = unassigned[0]
                    if abs(lit) not in assignment:
                        assignment[abs(lit)] = lit > 0
                        changed = True
        return assignment

    def dpll(assignment, clauses):
        assignment = unit_propagate(assignment, clauses)
        for clause in clauses:
            if all(abs(lit) in assignment and (lit > 0) != assignment[abs(lit)] for lit in clause):
                return 0
        if all(abs(lit) in assignment for clause in clauses for lit in clause):
            return 1
        for clause in clauses:
            for lit in clause:
                if abs(lit) not in assignment:
                    new_assignment = assignment.copy()
                    new_assignment[abs(lit)] = lit > 0
                    count = dpll(new_assignment, clauses)
                    new_assignment[abs(lit)] = lit < 0
                    count += dpll(new_assignment, clauses)
                    return count
        return 0

    return dpll({}, clauses)

def generate_tseitin_clauses(adj, charge, n):
    clauses = []
    for u in range(n):
        neighbors = adj[u]
        for i in range(3):
            for j in range(i + 1, 3):
                v1, v2 = neighbors[i], neighbors[j]
                clauses.append([u + 1, -v1 - 1, -v2 - 1])
                clauses.append([-(u + 1), v1 + 1, v2 + 1])
    for u in range(n):
        if charge[u] == 1:
            clauses.append([u + 1])
        else:
            clauses.append([-(u + 1)])
    return clauses

def run_trial(seed):
    n_values = [6, 8, 10, 12]
    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    first_failing_seed = None

    for n in n_values:
        adj = generate_3_regular_graph(n, seed)
        if adj is None or not is_connected(adj, n):
            continue
        charge = generate_charge(n, seed)
        partition = greedy_t_join(adj, charge, n)
        rho = compute_rho(partition)
        if rho == 0:
            continue
        clauses = generate_tseitin_clauses(adj, charge, n)
        t_star = dpll_sat_count(clauses, n)
        if t_star == 0:
            continue
        r = (math.log2(t_star) * math.log2(n + 2)) / rho
        metric_values.append(r)
        instances_tested += 1
        if r < 0.15:
            conjecture_holds = False
            counterexample = f"n={n}, seed={seed}, r={r}"
            if first_failing_seed is None:
                first_failing_seed = seed

    if not metric_values:
        return {
            "metric_name": "r(G,ω)",
            "metric_value": 0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }

    min_r = min(metric_values)
    if min_r < 0.15:
        conjecture_holds = False
        counterexample = f"min r={min_r} < 0.15"

    return {
        "metric_name": "r(G,ω)",
        "metric_value": min_r,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = sys.argv[1:] if len(sys.argv) > 1 else [random.randint(1, 1000) for _ in range(30)]
    seeds = [int(seed) for seed in seeds]

    metric_values = []
    instances_tested = 0
    conjecture_holds_all = True
    counterexample = ""
    first_failing_seed = None

    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        metric_values.append(trial["metric_value"])
        instances_tested += trial["instances_tested"]
        if not trial["conjecture_holds"]:
            conjecture_holds_all = False
            if counterexample == "":
                counterexample = trial["counterexample"]
            if first_failing_seed is None:
                first_failing_seed = seed

    if not metric_values:
        print("RESULT: INCONCLUSIVE reason=no_valid_instances")
        sys.exit(0)

    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = (sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values)) ** 0.5
    support_fraction = sum(1 for x in metric_values if x >= 0.15) / len(metric_values)

    if conjecture_holds_all:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")