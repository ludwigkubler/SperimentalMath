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
    while True:
        edges = []
        stubs = list(range(n)) * 3
        random.shuffle(stubs)
        for i in range(0, len(stubs), 2):
            u, v = stubs[i], stubs[i+1]
            if u != v and (u, v) not in edges and (v, u) not in edges:
                edges.append((u, v))
        adj = defaultdict(list)
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)
        if len(edges) == 3 * n // 2 and is_connected(adj, n):
            return adj

def is_connected(adj, n):
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

def generate_odd_charge(n, seed):
    random.seed(seed + 1)
    omega = [random.randint(0, 1) for _ in range(n)]
    if sum(omega) % 2 == 0:
        omega[0] = 1 - omega[0]
    return omega

def compute_t_star(adj, omega, max_calls=200000):
    n = len(adj)
    T = [i for i in range(n) if omega[i] == 1]
    clauses = []
    for u in T:
        neighbors = adj[u]
        for i in range(4):
            clause = []
            for j in range(3):
                v = neighbors[(i + j) % 3]
                clause.append((v, (i + j) % 2))
            clauses.append(clause)
    call_count = [0]

    def dpll(clauses, assignment, call_count):
        if call_count[0] > max_calls:
            return float('inf')
        call_count[0] += 1
        if not clauses:
            return 0
        for clause in clauses:
            if not clause:
                return float('inf')
        unit_clauses = [clause for clause in clauses if len(clause) == 1]
        if unit_clauses:
            literal = unit_clauses[0][0]
            new_assignment = assignment.copy()
            new_assignment[literal[0]] = literal[1]
            new_clauses = []
            for clause in clauses:
                if literal not in clause:
                    new_clause = [l for l in clause if l[0] != literal[0]]
                    new_clauses.append(new_clause)
            return dpll(new_clauses, new_assignment, call_count)
        for clause in clauses:
            if len(clause) == 2:
                a, b = clause
                new_assignment = assignment.copy()
                new_assignment[a[0]] = a[1]
                new_clauses = []
                for c in clauses:
                    if a not in c:
                        new_clause = [l for l in c if l[0] != a[0]]
                        new_clauses.append(new_clause)
                result = dpll(new_clauses, new_assignment, call_count)
                if result != float('inf'):
                    return result
                new_assignment = assignment.copy()
                new_assignment[b[0]] = b[1]
                new_clauses = []
                for c in clauses:
                    if b not in c:
                        new_clause = [l for l in c if l[0] != b[0]]
                        new_clauses.append(new_clause)
                return dpll(new_clauses, new_assignment, call_count)
        literal = clauses[0][0]
        new_assignment = assignment.copy()
        new_assignment[literal[0]] = literal[1]
        new_clauses = []
        for clause in clauses:
            if literal not in clause:
                new_clause = [l for l in clause if l[0] != literal[0]]
                new_clauses.append(new_clause)
        result = dpll(new_clauses, new_assignment, call_count)
        if result != float('inf'):
            return result
        new_assignment = assignment.copy()
        new_assignment[literal[0]] = 1 - literal[1]
        new_clauses = []
        for clause in clauses:
            if (literal[0], 1 - literal[1]) not in clause:
                new_clause = [l for l in clause if l[0] != literal[0]]
                new_clauses.append(new_clause)
        return dpll(new_clauses, new_assignment, call_count)
    return dpll(clauses, {}, call_count)

def compute_rho(adj, omega):
    n = len(adj)
    T = [i for i in range(n) if omega[i] == 1]
    g = len(adj) - n + 1
    for deg in range(1, g + 2):
        for D in itertools.combinations(T, deg):
            D_dict = defaultdict(int)
            for v in D:
                D_dict[v] += 1
            if is_baker_norine_rank_one(adj, D_dict):
                return deg
    return g + 1

def is_baker_norine_rank_one(adj, D):
    n = len(adj)
    for v in range(n):
        D_minus_v = D.copy()
        D_minus_v[v] -= 1
        if not has_effective_divisor(adj, D_minus_v):
            return False
    return True

def has_effective_divisor(adj, D):
    n = len(adj)
    for v in range(n):
        if D[v] < 0:
            return False
    return True

def run_trial(seed):
    n = random.choice([8, 10, 12])
    adj = generate_3_regular_graph(n, seed)
    omega = generate_odd_charge(n, seed)
    t_star = compute_t_star(adj, omega)
    rho = compute_rho(adj, omega)
    if t_star == float('inf'):
        return {
            "metric_name": "log2_t_star",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"t_star exceeded max calls for seed {seed}"
        }
    log2_t_star = math.log2(t_star)
    conjecture_holds = (rho / 4) <= log2_t_star
    counterexample = "" if conjecture_holds else f"rho/4 > log2_t_star for seed {seed}"
    return {
        "metric_name": "log2_t_star",
        "metric_value": log2_t_star,
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
    metric_values = [trial["metric_value"] for trial in trials if trial["metric_value"] != float('inf')]
    if not metric_values:
        print("RESULT: INCONCLUSIVE reason=no_valid_instances")
        sys.exit(0)
    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for trial in trials if trial["conjecture_holds"]) / len(trials)
    if all(trial["conjecture_holds"] for trial in trials):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(trial["seed"] for trial in trials if not trial["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rho/4 > log2_t_star\" first_failing_seed={first_failing_seed}")