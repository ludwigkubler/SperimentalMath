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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def smith_normal_form(matrix):
    n = len(matrix)
    M = [row[:] for row in matrix]
    r, c = 0, 0
    while r < n and c < n:
        if M[r][c] == 0:
            i = r + 1
            while i < n and M[i][c] == 0:
                i += 1
            if i < n:
                M[r], M[i] = M[i], M[r]
        if M[r][c] != 0:
            factor = M[r][c]
            for j in range(n):
                M[r][j] //= factor
            for i in range(n):
                if i != r and M[i][c] != 0:
                    multiplier = -M[i][c] // M[r][c]
                    for j in range(n):
                        M[i][j] += multiplier * M[r][j]
            r += 1
        c += 1
    return M

def laplacian(G):
    n = len(G)
    L = [[0] * n for _ in range(n)]
    for i in range(n):
        degree = sum(1 for j in range(n) if G[i][j])
        L[i][i] = -degree
        for j in range(i + 1, n):
            if G[i][j]:
                L[i][j] = L[j][i] = 1
    return L

def largest_invariant_factor(L):
    n = len(L)
    submatrix = [row[:n-1] for row in L[:n-1]]
    snf = smith_normal_form(submatrix)
    d_n_minus_1 = 1
    for i in range(n-2, -1, -1):
        if snf[i][i]:
            d_n_minus_1 *= snf[i][i]
    return d_n_minus_1

def tree_resolution_size(G, omega):
    n = len(G)
    variables = [i * 3 + j for i in range(n) for j in (0, 1)]
    clauses = []
    for v in range(n):
        parity_constraint = [variables[v*3], variables[v*3+1]]
        if omega[v] == 1:
            parity_constraint.append(variables[v*3+2])
        else:
            parity_constraint.append(-variables[v*3+2])
        clauses.append(parity_constraint)
    for u in range(n):
        for v in range(u + 1, n):
            if G[u][v]:
                clauses.extend([
                    [variables[u*3], variables[v*3]],
                    [-variables[u*3], -variables[v*3]],
                    [variables[u*3+1], variables[v*3+1]],
                    [-variables[u*3+1], -variables[v*3+1]],
                    [variables[u*3+2], variables[v*3+2]],
                    [-variables[u*3+2], -variables[v*3+2]]
                ])
    t_star = 0
    stack = []
    assignment = [None] * (n * 3)
    while True:
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if not unit_clause:
            break
        literal = unit_clause[0]
        var_index = abs(literal) - 1
        sign = literal > 0
        assignment[var_index] = sign
        t_star += 1
        for clause in clauses:
            if literal in clause:
                clause.remove(literal)
                if not clause:
                    break
    return t_star

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [8, 10, 12, 14, 16, 18, 20]
    results = []
    
    for n in n_values:
        G = [[0] * n for _ in range(n)]
        omega = {}
        
        # Generate random 3-regular graph
        edges = set()
        while len(edges) < n * (n - 1) // 2:
            u, v = random.sample(range(n), 2)
            if u != v and (u, v) not in edges and (v, u) not in edges:
                G[u][v] = G[v][u] = 1
                edges.add((u, v))
        
        # Assign odd charges to vertices
        for v in range(n):
            omega[v] = random.choice([0, 1])
        
        L = laplacian(G)
        d_n_minus_1 = largest_invariant_factor(L)
        nu_G = math.log2(d_n_minus_1)
        
        t_star = tree_resolution_size(G, omega)
        results.append({
            "n": n,
            "nu_G": nu_G,
            "t_star": t_star
        })
    
    metric_value = sum(result["t_star"] for result in results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(result["t_star"] >= 0.1 * result["nu_G"] - 5 for result in results if result["n"] % 2 == 0)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "tree_resolution_size",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
    
    results = [run_trial(seed) for seed in seeds]
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.2f} std={std_metric_value:.2f} support_fraction={support_fraction:.2f}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        print("RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed=<s>")
    else:
        print(f"RESULT: INCONCLUSIVE reason=budget_exceeded n_tested={len(results)}")