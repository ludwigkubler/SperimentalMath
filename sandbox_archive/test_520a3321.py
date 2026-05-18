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
    edges = []
    degrees = [0] * n
    while sum(degrees) < 2 * n:
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        if u != v and degrees[u] < 3 and degrees[v] < 3:
            edges.append((u, v))
            degrees[u] += 1
            degrees[v] += 1
    adj = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return adj

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

def generate_odd_charge(n, seed):
    random.seed(seed + 1)
    omega = [random.randint(0, 1) for _ in range(n)]
    if sum(omega) % 2 == 0:
        omega[0] = 1 - omega[0]
    return omega

def compute_t_star(adj, omega, n, max_calls=200000):
    T = [i for i in range(n) if omega[i] == 1]
    clauses = []
    for u in T:
        neighbors = adj[u]
        for v in neighbors:
            for w in neighbors:
                if v < w:
                    clauses.append((u, v, w))
    call_count = 0
    def dpll(clauses, assignment):
        nonlocal call_count
        call_count += 1
        if call_count > max_calls:
            return float('inf')
        if not clauses:
            return 0
        for clause in clauses:
            if all(var in assignment for var in clause):
                continue
            if any(-var in assignment for var in clause):
                continue
            break
        else:
            return 0
        for var in clause:
            if -var not in assignment:
                new_assignment = assignment.copy()
                new_assignment.add(var)
                new_clauses = [c for c in clauses if var not in c]
                result = dpll(new_clauses, new_assignment)
                if result != float('inf'):
                    return result + 1
        return float('inf')
    t_star = dpll(clauses, set())
    return t_star

def compute_rho(adj, omega, n):
    T = [i for i in range(n) if omega[i] == 1]
    g = len(adj) - n + 1
    for deg in range(1, g + 2):
        for D in itertools.combinations(T, deg):
            D = list(D)
            for v in range(n):
                if v not in D:
                    D_minus_v = D.copy()
                    D_minus_v.remove(v)
                    if dhar_burning(adj, D_minus_v, n):
                        return deg
    return g + 1

def dhar_burning(adj, D, n):
    for v in range(n):
        if v in D:
            continue
        D_minus_v = D.copy()
        D_minus_v.remove(v)
        if not is_linearly_equivalent(adj, D_minus_v, n):
            return False
    return True

def is_linearly_equivalent(adj, D, n):
    visited = [False] * n
    stack = [D[0]]
    visited[D[0]] = True
    count = 1
    while stack:
        u = stack.pop()
        for v in adj[u]:
            if v in D and not visited[v]:
                visited[v] = True
                stack.append(v)
                count += 1
    return count == len(D)

def run_trial(seed):
    n_values = [8, 10, 12]
    metric_values = []
    rho_values = []
    t_star_values = []
    for n in n_values:
        adj = generate_3_regular_graph(n, seed)
        if not is_connected(adj, n):
            continue
        omega = generate_odd_charge(n, seed)
        t_star = compute_t_star(adj, omega, n)
        rho = compute_rho(adj, omega, n)
        metric_values.append(math.log2(t_star) if t_star != float('inf') else float('inf'))
        rho_values.append(rho)
        t_star_values.append(t_star)
    if not metric_values:
        return {
            "metric_name": "log2_t_star_minus_rho_over_4",
            "metric_value": float('nan'),
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }
    metric_value = min(metric_values)
    rho_value = min(rho_values)
    t_star_value = min(t_star_values)
    conjecture_holds = (rho_value / 4 <= metric_value) if t_star_value != float('inf') else False
    counterexample = f"rho/4 > log2 t*: {rho_value}/4 > {metric_value}" if not conjecture_holds else ""
    return {
        "metric_name": "log2_t_star_minus_rho_over_4",
        "metric_value": metric_value,
        "instances_tested": len(n_values),
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
    conjecture_holds = [trial["conjecture_holds"] for trial in trials]
    if not metric_values:
        print("RESULT: INCONCLUSIVE reason=no_valid_instances")
        sys.exit(0)
    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(conjecture_holds) / len(conjecture_holds)
    if all(conjecture_holds):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        for trial in trials:
            if not trial["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{trial['counterexample']}\" first_failing_seed={seeds[trials.index(trial)]}")
                break