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

def generate_3_regular_graph(n):
    if n % 2 != 0:
        raise ValueError("n must be even for a 3-regular graph")
    edges = []
    vertices = list(range(n))
    random.shuffle(vertices)
    for i in range(0, n, 2):
        edges.append((vertices[i], vertices[i+1]))
    for i in range(n):
        edges.append((vertices[i], vertices[(i+1)%n]))
    return edges

def is_odd_sum_charge(G, c):
    n = len(set(itertools.chain(*G)))
    return sum(c[v] for v in range(n)) % 2 != 0

def generate_odd_sum_charge(n):
    c = [random.randint(0, 1) for _ in range(n)]
    while sum(c) % 2 == 0:
        c[random.randint(0, n-1)] ^= 1
    return c

def matching_polynomial(G):
    n = len(set(itertools.chain(*G)))
    adj = defaultdict(list)
    for u, v in G:
        adj[u].append(v)
        adj[v].append(u)
    dp = [[0] * (1 << n) for _ in range(n)]
    for mask in range(1 << n):
        for u in range(n):
            if mask & (1 << u):
                continue
            dp[u][mask] = 1
            for v in adj[u]:
                if mask & (1 << v):
                    continue
                dp[u][mask] += dp[v][mask | (1 << u)]
    mu = [0] * (n + 1)
    for u in range(n):
        mu[0] += dp[u][1 << u]
    for k in range(1, n + 1):
        for mask in range(1 << n):
            if bin(mask).count('1') != k:
                continue
            for u in range(n):
                if mask & (1 << u):
                    continue
                mu[k] += dp[u][mask]
    return mu

def mahler_measure(mu):
    roots = []
    for k in range(len(mu)):
        if mu[k] != 0:
            roots.extend([1] * mu[k])
    M = 1.0
    for r in roots:
        if r >= 1:
            M *= r
    return M

def encode_tseitin_cnf(G, c):
    n = len(set(itertools.chain(*G)))
    clauses = []
    for u, v in G:
        clauses.append([u, v])
        clauses.append([-u, -v])
    for u in range(n):
        clauses.append([u, -u])
    for u in range(n):
        if c[u] == 1:
            clauses.append([u])
        else:
            clauses.append([-u])
    return clauses

def dpll(clauses, order):
    n = len(order)
    assignment = [0] * n
    nodes = 0
    def backtrack():
        nonlocal nodes
        nodes += 1
        if all(any(lit != 0 and (lit > 0) == (assignment[abs(lit)-1] == 1) for lit in clause) for clause in clauses):
            return True
        for lit in order:
            if assignment[abs(lit)-1] == 0:
                assignment[abs(lit)-1] = 1 if lit > 0 else -1
                if backtrack():
                    return True
                assignment[abs(lit)-1] = -1 if lit > 0 else 1
                if backtrack():
                    return True
                assignment[abs(lit)-1] = 0
                return False
        return False
    backtrack()
    return nodes

def run_trial(seed):
    random.seed(seed)
    n = random.choice([8, 10, 12, 14, 16])
    G = generate_3_regular_graph(n)
    c = generate_odd_sum_charge(n)
    mu = matching_polynomial(G)
    M = mahler_measure(mu)
    clauses = encode_tseitin_cnf(G, c)
    orderings = [random.sample(range(-n, 0) + range(1, n+1), 2*n) for _ in range(10)]
    T_values = [dpll(clauses, order) for order in orderings]
    T = sorted(T_values)[len(T_values)//2]
    conjecture_holds = T >= M / 2
    counterexample = f"G={G}, c={c}, T={T}, M={M}" if not conjecture_holds else ""
    return {
        "metric_name": "log2_T_minus_log2_M",
        "metric_value": math.log2(T) - math.log2(M),
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
    if support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = seeds[next(i for i, r in enumerate(results) if not r["conjecture_holds"])]
        counterexample = results[next(i for i, r in enumerate(results) if not r["conjecture_holds"])]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_instances")