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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def is_connected(G):
        n = len(G)
        visited = [False] * n
        stack = [0]
        while stack:
            u = stack.pop()
            if not visited[u]:
                visited[u] = True
                for v in G[u]:
                    if not visited[v]:
                        stack.append(v)
        return all(visited)
    
    def spectral_gap(G):
        A = adjacency_matrix(G)
        eigenvalues_A = eigenvalues(A)
        lambda_max = max(eigenvalue for eigenvalue in eigenvalues_A)
        lambda_min = min(eigenvalue for eigenvalue in eigenvalues_A if eigenvalue != 0)
        return (lambda_max - lambda_min) / (2 * lambda_max)
    
    def adjacency_matrix(G):
        n = len(G)
        A = [[0] * n for _ in range(n)]
        for u, neighbors in enumerate(G):
            for v in neighbors:
                A[u][v] = 1
                A[v][u] = 1
        return A
    
    def eigenvalues(A):
        n = len(A)
        if n == 0:
            return []
        
        # Compute the characteristic polynomial using Gaussian elimination
        M = [A[i] + [-A[0][i]] for i in range(1, n)]
        det = A[0][0]
        for i in range(n):
            pivot_row = next((j for j in range(i, n) if M[j][i]), None)
            if pivot_row is None:
                return [Fraction(det)]  # All minors are zero
            if pivot_row != i:
                M[i], M[pivot_row] = M[pivot_row], M[i]
                det *= -1
            for j in range(i + 1, n):
                factor = Fraction(M[j][i], M[i][i])
                M[j] = [M[j][k] - factor * M[i][k] for k in range(n)]
        
        # Extract the eigenvalues from the diagonal of the reduced matrix
        return [Fraction(det) if i == 0 else Fraction(0) for i in range(n)]
    
    def dhar_burning(G, c, q):
        n = len(G)
        r_BN = sum(c[v] for v in G[q])
        queue = [q]
        visited = {q}
        while queue:
            u = queue.pop()
            for v in G[u]:
                if v not in visited and c[v] % 2 == 1:
                    visited.add(v)
                    r_BN += c[v]
                    queue.append(v)
        return r_BN
    
    def tseitin_cnf(G, c):
        n = len(G)
        clauses = []
        for u in range(n):
            if c[u] % 2 == 1:
                clauses.append([u + 1])
            else:
                clauses.append([-u - 1])
        for u in range(n):
            for v in G[u]:
                clauses.append([-(u + 1), -(v + 1)])
                clauses.append([u + 1, v + 1])
                clauses.append([-(u + 1), v + 1])
                clauses.append([u + 1, -(v + 1)])
        return clauses
    
    def dpll(clauses):
        n = len(clauses)
        assignment = [None] * (n + 1)
        
        def backtrack(level=0):
            if level == n:
                return True
            for literal in range(1, n + 1):
                if assignment[literal] is None:
                    assignment[literal] = True
                    if all(not unit_clause(literal) for clause in clauses):
                        if backtrack(level + 1):
                            return True
                    assignment[literal] = False
                    if all(not unit_clause(-literal) for clause in clauses):
                        if backtrack(level + 1):
                            return True
            return False
        
        def unit_clause(literal):
            return any(l == literal or l == -literal for clause in clauses)
        
        return backtrack()
    
    n_values = [8, 10, 12, 14]
    results = []
    for n in n_values:
        for _ in range(30):
            G = random_graph(n, 3)
            if not is_connected(G) or spectral_gap(G) < 0.15:
                continue
            
            c = [random.choice([0, 1]) for _ in range(n)]
            if sum(c) % 2 == 0:
                continue
            
            r_BN = dhar_burning(G, c, 0)
            D = g(G) - r_BN
            Tseitin_G_c = tseitin_cnf(G, c)
            
            L = 0
            W = 0
            if dpll(Tseitin_G_c):
                L = len([x for x in Tseitin_G_c if x[0] > 0])
                W = max(len(clause) for clause in Tseitin_G_c if clause[0] > 0)
            
            results.append({
                "metric_name": "D(G,c)",
                "metric_value": D,
                "instances_tested": len(results),
                "conjecture_holds": (1/3 <= math.log2(L) / D <= 3 and 1/3 <= W / D <= 3),
                "counterexample": ""
            })
    
    mean_D = sum(result["metric_value"] for result in results) / len(results)
    std_D = math.sqrt(sum((result["metric_value"] - mean_D) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "seed": seed,
        "mean_D": mean_D,
        "std_D": std_D,
        "support_fraction": support_fraction
    }

def random_graph(n, d):
    G = [[] for _ in range(n)]
    edges_added = 0
    while edges_added < n * d / 2:
        u, v = random.sample(range(n), 2)
        if u != v and v not in G[u]:
            G[u].append(v)
            G[v].append(u)
            edges_added += 1
    return G

def g(G):
    n = len(G)
    m = sum(len(neighbors) for neighbors in G) // 2
    return m - n + 1

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [3, 5, 7, 11, 13, 17, 19, 23, 29, 31] * 3
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    results = [run_trial(seed) for seed in seeds]
    mean_D = sum(result["mean_D"] for result in results) / len(results)
    std_D = math.sqrt(sum((result["mean_D"] - mean_D) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["support_fraction"] >= 0.8) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_D} std={std_D} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["support_fraction"] < 0.8)
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")