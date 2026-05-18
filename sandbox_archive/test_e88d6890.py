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
from collections import defaultdict
from fractions import Fraction

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
        omega[random.randint(0, n-1)] ^= 1
    return omega

def compute_tseitin_dpll_size(adj, omega, n, max_calls=200000):
    class DPLL:
        def __init__(self, adj, omega):
            self.adj = adj
            self.omega = omega
            self.n = len(adj)
            self.clauses = []
            self.calls = 0
            self.max_calls = max_calls
            self.build_clauses()

        def build_clauses(self):
            for u in range(self.n):
                neighbors = self.adj[u]
                if len(neighbors) != 3:
                    raise ValueError("Graph is not 3-regular")
                a, b, c = neighbors
                self.clauses.append([(u, 1), (a, 1), (b, 1), (c, 1)])
                self.clauses.append([(u, 0), (a, 0), (b, 1), (c, 1)])
                self.clauses.append([(u, 0), (a, 1), (b, 0), (c, 1)])
                self.clauses.append([(u, 0), (a, 1), (b, 1), (c, 0)])

        def dpll(self, assignment):
            self.calls += 1
            if self.calls > self.max_calls:
                return float('inf')

            if self.is_satisfied(assignment):
                return 0

            if not self.is_consistent(assignment):
                return float('inf')

            var = self.select_variable(assignment)
            if var is None:
                return float('inf')

            size1 = self.dpll(assignment + [(var, 1)])
            size2 = self.dpll(assignment + [(var, 0)])
            return 1 + min(size1, size2)

        def is_satisfied(self, assignment):
            for clause in self.clauses:
                satisfied = False
                for lit in clause:
                    if lit in assignment:
                        satisfied = True
                        break
                if not satisfied:
                    return False
            return True

        def is_consistent(self, assignment):
            for lit in assignment:
                if (lit[0], 1 - lit[1]) in assignment:
                    return False
            return True

        def select_variable(self, assignment):
            assigned_vars = {lit[0] for lit in assignment}
            for clause in self.clauses:
                unassigned = [lit for lit in clause if lit[0] not in assigned_vars]
                if len(unassigned) == 1:
                    return unassigned[0][0]
            for u in range(self.n):
                if u not in assigned_vars:
                    return u
            return None

    dpll = DPLL(adj, omega)
    size = dpll.dpll([])
    return size if size != float('inf') else max_calls

def compute_rho(adj, omega, n):
    T = [u for u in range(n) if omega[u] == 1]
    g = len(adj) - n + 1
    for deg in range(1, g + 2):
        for D in itertools.combinations(T, deg):
            D = list(D)
            if dhar_burning(adj, D, n):
                return deg
    return g + 1

def dhar_burning(adj, D, n):
    for v in range(n):
        D_minus_v = D.copy()
        if v in D_minus_v:
            D_minus_v.remove(v)
        if not is_linearly_equivalent(adj, D_minus_v, n):
            return False
    return True

def is_linearly_equivalent(adj, D, n):
    if not D:
        return True
    visited = [False] * n
    stack = D.copy()
    for u in stack:
        visited[u] = True
    while stack:
        u = stack.pop()
        for v in adj[u]:
            if not visited[v]:
                visited[v] = True
                stack.append(v)
    return all(visited[u] for u in range(n))

def run_trial(seed):
    n = random.choice([8, 10, 12])
    adj = generate_3_regular_graph(n, seed)
    omega = generate_odd_charge(n, seed)
    t_size = compute_tseitin_dpll_size(adj, omega, n)
    rho = compute_rho(adj, omega, n)
    log_t_size = math.log2(t_size) if t_size > 0 else 0
    conjecture_holds = (rho / 4) <= log_t_size
    counterexample = f"rho={rho}, log_t_size={log_t_size}" if not conjecture_holds else ""
    return {
        "metric_name": "log2_t_size",
        "metric_value": log_t_size,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample,
        "rho": rho,
        "t_size": t_size
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    trials = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        trials.append(trial)

    metric_values = [trial["metric_value"] for trial in trials]
    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for trial in trials if trial["conjecture_holds"]) / len(trials)

    if all(trial["conjecture_holds"] for trial in trials):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        failing_trials = [trial for trial in trials if not trial["conjecture_holds"]]
        first_failing_seed = seeds[trials.index(failing_trials[0])]
        print(f"RESULT: FALSIFIED counterexample=\"{failing_trials[0]['counterexample']}\" first_failing_seed={first_failing_seed}")