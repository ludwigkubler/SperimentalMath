# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def is_connected(G):
    visited = set()
    stack = [0]
    while stack:
        u = stack.pop()
        if u not in visited:
            visited.add(u)
            for v in G[u]:
                if v not in visited:
                    stack.append(v)
    return len(visited) == len(G)

def laplacian_matrix(G):
    n = len(G)
    L = [[0] * n for _ in range(n)]
    degree_sum = sum(len(neighbors) for neighbors in G.values())
    for u, neighbors in enumerate(G):
        L[u][u] = -len(neighbors)
        for v in neighbors:
            L[u][v] += 1
    return L

def smith_normal_form(M):
    n = len(M)
    U, V = [[0] * n for _ in range(n)], [[0] * n for _ in range(n)]
    for i in range(n):
        U[i][i], V[i][i] = 1, 1
    for k in range(n):
        # Find pivot
        pivot_row, pivot_col = -1, -1
        for i in range(k, n):
            for j in range(k, n):
                if M[i][j] != 0:
                    pivot_row, pivot_col = i, j
                    break
            if pivot_row != -1:
                break
        
        # Swap rows to make the pivot non-zero
        if pivot_row != k:
            M[k], M[pivot_row] = M[pivot_row], M[k]
            U[k], U[pivot_row] = U[pivot_row], U[k]
        
        # Make the pivot 1
        factor = M[k][k]
        for j in range(n):
            M[k][j] //= factor
            U[k][j] //= factor
        
        # Eliminate below and above the pivot
        for i in range(k + 1, n):
            factor = M[i][k]
            for j in range(n):
                M[i][j] -= factor * M[k][j]
                U[i][j] -= factor * U[k][j]
        
        for i in range(k - 1, -1, -1):
            factor = M[i][k]
            for j in range(n):
                M[i][j] -= factor * M[k][j]
                U[i][j] -= factor * U[k][j]
    
    return M, U, V

def dpll(G, assignment, unit_clause=None):
    if unit_clause is not None:
        u, v = unit_clause
        if v in G[u]:
            assignment[v] = 1
        else:
            assignment[v] = 0
    
    # Unit propagation
    while True:
        changed = False
        for v in range(len(G)):
            if assignment[v] is not None:
                continue
            ones, zeros = 0, 0
            for u in G[v]:
                if assignment[u] == 1:
                    ones += 1
                elif assignment[u] == 0:
                    zeros += 1
            if ones == len(G[v]):
                assignment[v] = 0
                changed = True
            elif zeros == len(G[v]) - 1:
                assignment[v] = 1
                changed = True
        if not changed:
            break
    
    # Pure literal elimination
    while True:
        changed = False
        for u in range(len(G)):
            ones, zeros = 0, 0
            for v in G[u]:
                if assignment[v] == 1:
                    ones += 1
                elif assignment[v] == 0:
                    zeros += 1
            if ones == len(G[u]):
                for v in G[u]:
                    if assignment[v] is None:
                        assignment[v] = 0
                        changed = True
            elif zeros == len(G[u]) - 1:
                for v in G[u]:
                    if assignment[v] is None:
                        assignment[v] = 1
                        changed = True
        if not changed:
            break
    
    # Backtracking
    stack = [(0, {})]
    while stack:
        u, assignment = stack.pop()
        if u == len(G):
            return True
        
        for v in G[u]:
            if assignment[v] is None:
                new_assignment = assignment.copy()
                new_assignment[v] = 1
                if dpll(G, new_assignment, (u, v)):
                    return True
                new_assignment[v] = 0
                stack.append((u + 1, new_assignment))
    
    return False

def tseitin_encoding(G, sigma):
    n = len(G)
    clauses = []
    for u in range(n):
        if sigma[u]:
            clauses.append([u])
        else:
            clauses.append([-u])
    
    for u in range(n):
        for v in G[u]:
            clauses.append([u, -v])
            clauses.append([-u, v])
    
    return clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    V = random.choice([8, 10, 12, 14, 16])
    G = {}
    while not is_connected(G):
        G.clear()
        for _ in range(V * (V - 1) // 2):
            u, v = random.sample(range(V), 2)
            if u != v and v not in G[u]:
                G.setdefault(u, []).append(v)
                G.setdefault(v, []).append(u)
    
    sigma = [i == 0 for i in range(V)]
    L = laplacian_matrix(G)
    M = [[L[i][j] % 2 for j in range(len(L))] for i in range(len(L))]
    k_2_G, _, _ = smith_normal_form(M)
    k_2_G = sum(1 for row in k_2_G if any(x != 0 for x in row))
    
    clauses = tseitin_encoding(G, sigma)
    assignment = [None] * V
    decision_nodes = 0
    
    def dpll_with_count(G, assignment, unit_clause=None):
        nonlocal decision_nodes
        if unit_clause is not None:
            u, v = unit_clause
            if v in G[u]:
                assignment[v] = 1
            else:
                assignment[v] = 0
        
        while True:
            changed = False
            for v in range(len(G)):
                if assignment[v] is not None:
                    continue
                ones, zeros = 0, 0
                for u in G[v]:
                    if assignment[u] == 1:
                        ones += 1
                    elif assignment[u] == 0:
                        zeros += 1
                if ones == len(G[v]):
                    assignment[v] = 0
                    changed = True
                elif zeros == len(G[v]) - 1:
                    assignment[v] = 1
                    changed = True
            if not changed:
                break
        
        while True:
            changed = False
            for u in range(len(G)):
                ones, zeros = 0, 0
                for v in G[u]:
                    if assignment[v] == 1:
                        ones += 1
                    elif assignment[v] == 0:
                        zeros += 1
                if ones == len(G[v]):
                    for v in G[u]:
                        if assignment[v] is None:
                            assignment[v] = 0
                            changed = True
                elif zeros == len(G[v]) - 1:
                    for v in G[u]:
                        if assignment[v] is None:
                            assignment[v] = 1
                            changed = True
            if not changed:
                break
        
        stack = [(0, {})]
        while stack:
            u, assignment = stack.pop()
            decision_nodes += 1
            if u == len(G):
                return True
            
            for v in G[u]:
                if assignment[v] is None:
                    new_assignment = assignment.copy()
                    new_assignment[v] = 1
                    if dpll_with_count(G, new_assignment, (u, v)):
                        return True
                    new_assignment[v] = 0
                    stack.append((u + 1, new_assignment))
        
        return False
    
    dpll_with_count(G, assignment)
    
    log_2_T_G_sigma = math.log2(decision_nodes) if decision_nodes > 0 else -math.inf
    
    return {
        "metric_name": "log_2 T(G,σ)",
        "metric_value": log_2_T_G_sigma,
        "instances_tested": 1,
        "conjecture_holds": log_2_T_G_sigma >= k_2_G,
        "counterexample": "" if log_2_T_G_sigma >= k_2_G else f"V={V}, k_2(G)={k_2_G}, T(G,σ)={decision_nodes}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(30))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")