# auto-injected by SEC sandbox
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import itertools
from fractions import Fraction

def matrix_mult(A, B):
    return [[sum(a * b for a, b in zip(row, col)) for col in zip(*B)] for row in A]

def matrix_add(A, B):
    return [[a + b for a, b in zip(row_a, row_b)] for row_a, row_b in zip(A, B)]

def matrix_sub(A, B):
    return [[a - b for a, b in zip(row_a, row_b)] for row_a, row_b in zip(A, B)]

def matrix_transpose(A):
    return [list(row) for row in zip(*A)]

def matrix_rank(A):
    if not A:
        return 0
    rank = 0
    for col in range(len(A[0])):
        pivot = -1
        for row in range(rank, len(A)):
            if A[row][col] != 0:
                pivot = row
                break
        if pivot == -1:
            continue
        A[rank], A[pivot] = A[pivot], A[rank]
        for row in range(rank + 1, len(A)):
            if A[row][col] != 0:
                factor = Fraction(A[row][col], A[rank][col])
                A[row] = [a - factor * b for a, b in zip(A[row], A[rank])]
        rank += 1
    return rank

def generate_3_regular_graph(n, seed):
    random.seed(seed)
    if n % 2 != 0:
        raise ValueError("n must be even for 3-regular graphs")
    edges = []
    stubs = list(range(n)) * 3
    while stubs:
        u = random.choice(stubs)
        stubs.remove(u)
        v = random.choice([x for x in stubs if x != u])
        stubs.remove(v)
        edges.append((u, v))
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    visited = [False] * n
    stack = [0]
    visited[0] = True
    while stack:
        u = stack.pop()
        for v in adj[u]:
            if not visited[v]:
                visited[v] = True
                stack.append(v)
    if not all(visited):
        return generate_3_regular_graph(n, seed + 1)
    return adj

def generate_odd_charge(n, seed):
    random.seed(seed)
    omega = [random.randint(0, 1) for _ in range(n)]
    if sum(omega) % 2 == 0:
        omega[0] = 1 - omega[0]
    return omega

def compute_t_star(adj, omega, max_calls=200000):
    n = len(adj)
    T = [i for i, o in enumerate(omega) if o == 1]
    clauses = []
    for u in range(n):
        neighbors = adj[u]
        clause = []
        for v in neighbors:
            clause.append((u, v))
        clauses.append(clause)
    call_count = 0
    def dpll(clauses, assignment):
        nonlocal call_count
        call_count += 1
        if call_count > max_calls:
            return float('inf')
        if not clauses:
            return 1
        for clause in clauses:
            if all((lit in assignment) and (assignment[lit] == False) for lit in clause):
                return 0
        unit_clauses = [c for c in clauses if len(c) == 1]
        while unit_clauses:
            lit = unit_clauses[0][0]
            assignment[lit] = True
            new_clauses = []
            for clause in clauses:
                if lit not in clause:
                    new_clause = [l for l in clause if l != (-lit,)]
                    if not new_clause:
                        return 0
                    new_clauses.append(new_clause)
            clauses = new_clauses
            unit_clauses = [c for c in clauses if len(c) == 1]
        if not clauses:
            return 1
        lit = clauses[0][0]
        return dpll([c for c in clauses if lit not in c], {**assignment, lit: True}) + \
               dpll([c for c in clauses if (-lit,) not in c], {**assignment, lit: False})
    t_star = dpll(clauses, {})
    return min(t_star, max_calls)

def compute_rho(adj, omega):
    n = len(adj)
    T = [i for i, o in enumerate(omega) if o == 1]
    g = len([(u, v) for u in range(n) for v in adj[u] if u < v]) - n + 1
    for deg in range(1, g + 2):
        for D in itertools.combinations(T, deg):
            D = list(D)
            for v in range(n):
                D_minus_v = [d for d in D if d != v]
                if len(D_minus_v) == len(D):
                    continue
                rank = dhar_burning(adj, D_minus_v)
                if rank >= 1:
                    return deg
    return g + 1

def dhar_burning(adj, D):
    n = len(adj)
    A = [[0] * n for _ in range(n)]
    for u in range(n):
        for v in adj[u]:
            A[u][v] = 1
    for d in D:
        A[d][d] = 1
    return matrix_rank(A)

def run_trial(seed):
    random.seed(seed)
    n = random.choice([8, 10, 12])
    adj = generate_3_regular_graph(n, seed)
    omega = generate_odd_charge(n, seed)
    t_star = compute_t_star(adj, omega)
    rho = compute_rho(adj, omega)
    if t_star <= 0:
        return {
            "metric_name": "log2_t_star_vs_rho",
            "metric_value": 0.0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"t_star={t_star} <= 0 for n={n}"
        }
    log2_t_star = math.log2(t_star)
    metric_value = log2_t_star - rho / 4
    conjecture_holds = metric_value >= 0
    counterexample = "" if conjecture_holds else f"rho/4={rho/4} > log2_t_star={log2_t_star} for n={n}"
    return {
        "metric_name": "log2_t_star_vs_rho",
        "metric_value": metric_value,
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
    metric_values = [t["metric_value"] for t in trials]
    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(t["conjecture_holds"] for t in trials) / len(trials)
    if all(t["conjecture_holds"] for t in trials):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(t["seed"] for t in trials if not t["conjecture_holds"])
        counterexample = next(t["counterexample"] for t in trials if not t["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")