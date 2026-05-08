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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def smith_normal_form(matrix):
    m, n = len(matrix), len(matrix[0])
    R, C = [1] * m, [1] * n
    for k in range(min(m, n)):
        i_max = max(range(k, m), key=lambda i: abs(matrix[i][k]))
        if matrix[i_max][k] == 0:
            continue
        R[k], R[i_max] = R[i_max], R[k]
        C[k], C[i_max] = C[i_max], C[k]
        for j in range(n):
            matrix[k][j] *= R[k]
        for i in range(m):
            matrix[i][k] *= C[k]
        pivot = matrix[k][k]
        for j in range(k + 1, n):
            matrix[k][j] //= pivot
        for i in range(m):
            if i != k:
                factor = matrix[i][k]
                for j in range(n):
                    matrix[i][j] -= factor * matrix[k][j]
    return matrix

def laplacian(G):
    V = len(G)
    L = [[0] * V for _ in range(V)]
    for u in range(V):
        degree = sum(1 for v in G[u] if v > u)
        L[u][u] = -degree
        for v in G[u]:
            if v > u:
                L[u][v] = 1
                L[v][u] = 1
    return L

def reduce_laplacian(L):
    V = len(L)
    L_reduced = [row[1:] for row in L[1:]]
    return L_reduced

def determinant(matrix):
    if len(matrix) == 1:
        return matrix[0][0]
    det = 0
    sign = 1
    for j in range(len(matrix[0])):
        submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
        det += sign * matrix[0][j] * determinant(submatrix)
        sign *= -1
    return det

def rank(matrix):
    snf = smith_normal_form(matrix)
    rank = 0
    for i in range(len(snf)):
        if snf[i][i] != 0:
            rank += 1
    return rank

def tseitin(G, sigma):
    V = len(G)
    literals = [chr(i) for i in range(97, 97 + V)]
    clauses = []
    for u in range(V):
        if sigma[u] == 1:
            clauses.append([literals[u]])
        else:
            clauses.append([-literals[u]])
        for v in G[u]:
            if v > u:
                clauses.append([literals[u], literals[v]])
                clauses.append([-literals[u], -literals[v]])
    return clauses

def dpll(clauses, assignment):
    if not clauses:
        return True
    unit_clauses = [c[0] for c in clauses if len(c) == 1]
    if not unit_clauses:
        return False
    literal = unit_clauses[0]
    new_assignment = assignment.copy()
    new_assignment[literal] = True
    new_clauses = []
    for clause in clauses:
        if literal in clause:
            continue
        if -literal in clause:
            new_clause = [l for l in clause if l != -literal]
            if not new_clause:
                return False
            new_clauses.append(new_clause)
        else:
            new_clauses.append(clause)
    if dpll(new_clauses, new_assignment):
        return True
    new_assignment[literal] = False
    new_clauses = []
    for clause in clauses:
        if -literal in clause:
            continue
        if literal in clause:
            new_clause = [l for l in clause if l != literal]
            if not new_clause:
                return False
            new_clauses.append(new_clause)
        else:
            new_clauses.append(clause)
    return dpll(new_clauses, new_assignment)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    V = random.choice([8, 10, 12, 14, 16])
    G = []
    while len(G) < V:
        u = random.randint(0, V-1)
        v = random.randint(0, V-1)
        if u != v and v not in G[u]:
            G.append(u)
            G[-1].append(v)
            G[v] = G[v] + [u]
    sigma = [0] * V
    sigma[0] = 1
    L = laplacian(G)
    L_reduced = reduce_laplacian(L)
    k_2 = rank(L_reduced)
    T_G_sigma = dpll(tseitin(G, sigma), {})
    log_2_T_G_sigma = math.log2(T_G_sigma) if T_G_sigma > 0 else -math.inf
    conjecture_holds = log_2_T_G_sigma >= k_2
    counterexample = "" if conjecture_holds else f"T(G,σ)={T_G_sigma}, k_2(G)={k_2}"
    return {
        "metric_name": "log_2 T(G,σ)",
        "metric_value": log_2_T_G_sigma,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")