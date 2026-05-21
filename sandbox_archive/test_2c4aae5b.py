# auto-injected by SEC sandbox
import itertools
import json
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from collections import defaultdict

def run_trial(seed: int) -> dict:
    n = random.choice([8, 10, 12, 14, 16, 18, 20])
    G = generate_random_3_regular_graph(n)
    c = assign_odd_weight_charge(G)
    Ts_G_c = expand_tseitin_xor_clauses(G, c)
    backtrack_count = dpll(Ts_G_c)
    
    X_G = build_X_G(G)
    up_laplacian = compute_up_laplacian(X_G)
    lambda_up = compute_lambda_up(up_laplacian)
    
    metric_value = math.log2(backtrack_count)
    instances_tested = 1
    conjecture_holds = False
    counterexample = ""
    
    if backtrack_count >= 0.8 * (0.05 * lambda_up * math.sqrt(n)):
        conjecture_holds = True
    
    return {
        "metric_name": "log2(backtrack_count)",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def generate_random_3_regular_graph(n):
    if n % 2 != 0:
        raise ValueError("n must be even")
    
    G = defaultdict(set)
    vertices = list(range(1, n + 1))
    random.shuffle(vertices)
    
    for i in range(n // 2):
        u, v = vertices[2 * i], vertices[2 * i + 1]
        G[u].add(v)
        G[v].add(u)
    
    return G

def assign_odd_weight_charge(G):
    n = len(G)
    c = {v: random.choice([0, 1]) for v in range(1, n + 1)}
    if sum(c.values()) % 2 == 0:
        c[random.randint(1, n)] ^= 1
    return c

def expand_tseitin_xor_clauses(G, c):
    clauses = []
    n = len(G)
    
    for v in range(1, n + 1):
        if c[v] == 1:
            clauses.append([v])
        else:
            clauses.append([-v])
    
    return clauses

def dpll(clauses):
    assignment = [0] * (len(clauses) + 1)
    backtrack_count = 0
    
    def unit_propagation():
        nonlocal backtrack_count
        while True:
            found_unit_clause = False
            for i, clause in enumerate(clauses):
                if len([x for x in clause if assignment[abs(x)] == 0]) == 1:
                    lit = next(x for x in clause if assignment[abs(x)] == 0)
                    assignment[abs(lit)] = 1 if lit > 0 else -1
                    found_unit_clause = True
            if not found_unit_clause:
                break
    
    def dpll_recursive():
        nonlocal backtrack_count
        unit_propagation()
        
        if all(assignment[x] != 0 for x in range(1, len(clauses) + 1)):
            return True
        
        v = next(x for x in range(1, len(clauses) + 1) if assignment[x] == 0)
        assignment[v] = 1
        if dpll_recursive():
            return True
        backtrack_count += 1
        assignment[v] = -1
        if dpll_recursive():
            return True
        
        return False
    
    return backtrack_count if not dpll_recursive() else backtrack_count

def build_X_G(G):
    X_G = []
    for u, v in G.items():
        for w in G[u]:
            if w > v:
                X_G.append((u, v, w))
    return X_G

def compute_up_laplacian(X_G):
    n = len(X_G)
    up_laplacian = [[0] * n for _ in range(n)]
    
    for i, (u, v, w) in enumerate(X_G):
        up_laplacian[i][i] += 1
        up_laplacian[(i + n) % (2 * n)][(i + n) % (2 * n)] += 1
    
    return up_laplacian

def compute_lambda_up(up_laplacian):
    n = len(up_laplacian)
    eigenvalues, eigenvectors = eigh(up_laplacian)
    lambda_up = min(eigenvalue for eigenvalue in eigenvalues if eigenvalue > 0)
    return lambda_up

def eigh(A):
    n = len(A)
    Q = [[0] * n for _ in range(n)]
    T = A.copy()
    
    def householder_vector(v, k):
        v[k] += math.sqrt(sum(x**2 for x in v[k:]))
        v /= v[k]
        return v
    
    def apply_householder(Q, T, k):
        v = householder_vector(T[k], k)
        Q[k] = v
        for i in range(k + 1, n):
            u = [T[i][j] - v[j] * (v[i] + v[j]) for j in range(n)]
            T[i] = u
            for j in range(i + 1, n):
                Q[j][i] = u[j]
    
    def qr_decomposition(Q, T):
        for k in range(n - 2, -1, -1):
            apply_householder(Q, T, k)
    
    qr_decomposition(Q, T)
    
    eigenvalues = [T[i][i] for i in range(n)]
    eigenvectors = Q
    
    return eigenvalues, eigenvectors

if __name__ == "__main__":
    seeds = list(map(int, sys.argv[1:])) if len(sys.argv) > 1 else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(result["metric_value"] < 0.8 * (0.05 * result["metric_value"] / math.sqrt(n)) for n, result in zip([8, 10, 12, 14, 16, 18, 20], results)):
        print(f"RESULT: FALSIFIED counterexample=\"backtrack_count < 0.8 * (0.05 * lambda_up * sqrt(n))\" first_failing_seed={seeds[results.index(next(result for result in results if result['metric_value'] < 0.8 * (0.05 * result['metric_value'] / math.sqrt(18))))]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")