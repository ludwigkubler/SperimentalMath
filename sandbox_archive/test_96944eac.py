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
        raise ValueError("n must be even for a 3-regular graph")
    edges = []
    degrees = [0] * n
    while len(edges) < 3 * n // 2:
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        if u != v and degrees[u] < 3 and degrees[v] < 3 and (u, v) not in edges and (v, u) not in edges:
            edges.append((u, v))
            degrees[u] += 1
            degrees[v] += 1
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return adj

def is_connected(adj):
    n = len(adj)
    visited = [False] * n
    queue = deque([0])
    visited[0] = True
    count = 1
    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if not visited[v]:
                visited[v] = True
                queue.append(v)
                count += 1
    return count == n

def generate_connected_3_regular_graph(n, seed):
    max_attempts = 100
    for _ in range(max_attempts):
        adj = generate_3_regular_graph(n, seed)
        if is_connected(adj):
            return adj
        seed += 1
    raise ValueError("Failed to generate connected 3-regular graph")

def generate_random_charge(n, seed):
    random.seed(seed)
    charge = [random.randint(0, 1) for _ in range(n)]
    if sum(charge) % 2 != 1:
        charge[random.randint(0, n - 1)] ^= 1
    return charge

def greedy_t_join(adj, charge):
    n = len(adj)
    odd_vertices = [v for v in range(n) if charge[v] == 1]
    if len(odd_vertices) % 2 == 1:
        odd_vertices.append(min(v for v in range(n) if charge[v] == 0))
    pairs = []
    while odd_vertices:
        u = odd_vertices.pop()
        min_dist = float('inf')
        closest_v = -1
        for v in odd_vertices:
            dist = bfs_distance(adj, u, v)
            if dist < min_dist or (dist == min_dist and v < closest_v):
                min_dist = dist
                closest_v = v
        if closest_v != -1:
            pairs.append(min_dist)
            odd_vertices.remove(closest_v)
    return pairs

def bfs_distance(adj, u, v):
    n = len(adj)
    visited = [-1] * n
    queue = deque([u])
    visited[u] = 0
    while queue:
        current = queue.popleft()
        if current == v:
            return visited[current]
        for neighbor in adj[current]:
            if visited[neighbor] == -1:
                visited[neighbor] = visited[current] + 1
                queue.append(neighbor)
    return float('inf')

def hook_length_dimension(partition):
    if not partition:
        return 0.0
    n = sum(partition)
    if n == 0:
        return 0.0
    log_dim = 0.0
    for part in partition:
        for i in range(1, part + 1):
            hook = part + len([p for p in partition if p >= i]) - i
            log_dim += math.log2(i) - math.log2(hook)
    return log_dim

def small_dpll(adj, charge, max_nodes=2**18):
    n = len(adj)
    clauses = []
    for u in range(n):
        neighbors = adj[u]
        for v in neighbors:
            if v > u:
                clauses.append([u, v])
    for u in range(n):
        if charge[u] == 1:
            clauses.append([u])
    num_vars = n
    num_clauses = len(clauses)
    def count_satisfying_assignments():
        def backtrack(assignment, remaining_clauses):
            if len(assignment) == num_vars:
                for clause in remaining_clauses:
                    if all(var not in assignment or assignment[var] == 0 for var in clause):
                        return 0
                return 1
            var = len(assignment)
            count = 0
            for val in [0, 1]:
                new_assignment = assignment.copy()
                new_assignment[var] = val
                new_remaining_clauses = [clause for clause in remaining_clauses if var not in clause or new_assignment[var] == 1]
                count += backtrack(new_assignment, new_remaining_clauses)
            return count
        return backtrack({}, clauses)
    return count_satisfying_assignments()

def run_trial(seed):
    n_values = [6, 8, 10, 12]
    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    for n in n_values:
        try:
            adj = generate_connected_3_regular_graph(n, seed)
            charge = generate_random_charge(n, seed)
            partition = greedy_t_join(adj, charge)
            rho = hook_length_dimension(partition)
            if rho <= 0:
                continue
            t_star = small_dpll(adj, charge)
            if t_star <= 0:
                continue
            log_t_star = math.log2(t_star)
            log_n_plus_2 = math.log2(n + 2)
            r = (log_t_star * log_n_plus_2) / rho
            metric_values.append(r)
            instances_tested += 1
            if r < 0.15:
                conjecture_holds = False
                counterexample = f"n={n}, seed={seed}, r={r}"
        except Exception as e:
            continue
    if not metric_values:
        return {
            "metric_name": "min_r",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }
    min_r = min(metric_values)
    return {
        "metric_name": "min_r",
        "metric_value": min_r,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample if not conjecture_holds else ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [random.randint(1, 1000) for _ in range(30)]
    metric_values = []
    instances_tested = 0
    conjecture_holds_all = True
    counterexample = ""
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        metric_values.append(trial["metric_value"])
        instances_tested += trial["instances_tested"]
        if not trial["conjecture_holds"]:
            conjecture_holds_all = False
            counterexample = trial["counterexample"]
    if not metric_values:
        print("RESULT: INCONCLUSIVE reason=no_valid_instances")
        sys.exit(0)
    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for x in metric_values if x >= 0.15) / len(metric_values)
    if conjecture_holds_all:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[metric_values.index(min(metric_values))]}")