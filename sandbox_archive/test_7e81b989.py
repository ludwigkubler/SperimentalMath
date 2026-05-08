# auto-injected by SEC sandbox
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def hashimoto_matrix(G):
    n, m = len(G), sum(len(v) for v in G.values()) // 2
    B = [[0] * (2 * m) for _ in range(2 * m)]
    edges = []
    for u, neighbors in G.items():
        for v in neighbors:
            if u < v:
                edges.append((u, v))
    for i, (u, v) in enumerate(edges):
        B[2 * i][2 * m + 2 * i] = 1
        B[2 * i + 1][2 * m + 2 * i + 1] = 1
        B[2 * m + 2 * i][2 * i] = 1
        B[2 * m + 2 * i + 1][2 * i + 1] = 1
    return B

def spectral_gap(B):
    eigenvalues = sorted(gaussian_elimination([[B[i][j] - (i == j) for j in range(len(B))] for i in range(len(B))]), key=abs)
    return abs(eigenvalues[-2])

def tseitin(G, sigma):
    n = len(G)
    clauses = []
    for u in G:
        if random.choice([0, 1]) == 0:
            clauses.append([u])
        else:
            clauses.append([-u])
    for u, neighbors in G.items():
        for v in neighbors:
            if u < v and (v - u) % sigma != 0:
                clauses.append([-u, v])
    return clauses

def dpll(clauses):
    stack = []
    def solve(i=0):
        if i == len(clauses):
            return True
        literals = set()
        for clause in clauses[i:]:
            literals.update(abs(l) for l in clause)
        literal = random.choice(list(literals))
        sign = 1 if literal > 0 else -1
        stack.append((literal, sign))
        new_clauses = []
        for clause in clauses[i:]:
            if any(l == -sign * literal for l in clause):
                continue
            elif all(abs(l) != abs(literal) for l in clause):
                return False
            else:
                new_clauses.append([l for l in clause if l != sign * literal])
        if solve(i + 1):
            return True
        stack.pop()
        stack.append((-literal, sign))
        new_clauses = []
        for clause in clauses[i:]:
            if any(l == sign * literal for l in clause):
                continue
            elif all(abs(l) != abs(literal) for l in clause):
                return False
            else:
                new_clauses.append([l for l in clause if l != -sign * literal])
        if solve(i + 1):
            return True
        stack.pop()
        return False
    return solve()

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([12, 16, 20, 24, 28])
    G = {}
    while len(G) < n:
        u, v = random.sample(range(n), 2)
        if u not in G:
            G[u] = []
        if v not in G:
            G[v] = []
        if v not in G[u]:
            G[u].append(v)
            G[v].append(u)
    sigma = random.choice([i for i in range(1, n) if i % 2 == 1])
    clauses = tseitin(G, sigma)
    cap = 2**22
    T = 0
    capped = False
    while not solved and len(stack) < cap:
        T += 1
        solve()
    if len(stack) >= cap:
        capped = True
    lambda_2_B = spectral_gap(hashimoto_matrix(G))
    nu_G = n * max(0, math.sqrt(2) - (lambda_2_B - math.sqrt(2))) / math.sqrt(2)
    log2_T = math.log2(T)
    return {
        "metric_name": "log2_T",
        "metric_value": log2_T,
        "instances_tested": 1,
        "conjecture_holds": log2_T >= nu_G / 16 or capped,
        "counterexample": "" if log2_T >= nu_G / 16 or capped else f"sigma={sigma}, n={n}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_T = sum(r["metric_value"] for r in results if not r["counterexample"])
    num_uncapped = sum(1 for r in results if not r["counterexample"])
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    spearman_rho = 0.5 * (2 * sum((r["metric_value"] - total_T / num_uncapped) ** 2 for r in results if not r["counterexample"])) / (num_uncapped - 1)
    
    if support_fraction >= 0.85 and spearman_rho >= 0.6:
        print(f"RESULT: SUPPORTED mean={total_T / num_uncapped} std=NA support_fraction={support_fraction}")
    elif any(r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"sigma={results[0]['counterexample']}, n={results[0]['metric_value']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE support_fraction_too_low")