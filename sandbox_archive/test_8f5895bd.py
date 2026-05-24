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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    
    # Generate a random planar graph with n vertices
    def is_planar(graph):
        if len(graph) <= 4:
            return True
        for u in range(len(graph)):
            neighbors = [v for v in range(len(graph)) if graph[u][v] != 0]
            if len(neighbors) >= 5:
                return False
            for i in range(len(neighbors)):
                for j in range(i + 1, len(neighbors)):
                    if any(graph[neighbors[i]][v] != 0 and graph[neighbors[j]][v] != 0 for v in range(len(graph))):
                        return False
        return True
    
    def add_edge(graph, u, v):
        graph[u][v] = 1
        graph[v][u] = 1
    
    def remove_edge(graph, u, v):
        graph[u][v] = 0
        graph[v][u] = 0
    
    def find_planar_graph(n):
        for _ in range(1000):  # Try up to 1000 times to generate a planar graph
            graph = [[0] * n for _ in range(n)]
            edges = set()
            while len(edges) < 3 * (n - 2):
                u, v = random.sample(range(n), 2)
                if u != v and (u, v) not in edges:
                    add_edge(graph, u, v)
                    edges.add((u, v))
            if is_planar(graph):
                return graph
        raise ValueError("Failed to generate a planar graph after 1000 attempts")
    
    try:
        G = find_planar_graph(n)
    except ValueError as e:
        return {
            "metric_name": "minimal_rank",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": str(e)
        }
    
    # Compute the Laplacian matrix L(G)
    L = [[0] * n for _ in range(n)]
    for u in range(n):
        degree = sum(1 for v in range(n) if G[u][v] != 0)
        L[u][u] = -degree
        for v in range(u + 1, n):
            L[u][v] = G[u][v]
            L[v][u] = G[v][u]
    
    # Tropicalize the Laplacian matrix T(L(G))
    def tropical_add(a, b):
        if a == float('inf') or b == float('inf'):
            return float('inf')
        return max(a, b)
    
    def tropical_multiply(a, b):
        if a == float('inf') or b == float('inf'):
            return float('inf')
        return a + b
    
    T_L = [[float('-inf')] * n for _ in range(n)]
    for u in range(n):
        for v in range(n):
            if u == v:
                T_L[u][v] = 0
            elif L[u][v] != 0:
                T_L[u][v] = tropical_multiply(L[u][v], -1)
    
    # Compute the minimal rank of T(L(G))
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i + 1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                return None
            for j in range(i + 1, n):
                factor = A[j][i] / A[i][i]
                for k in range(i, n):
                    A[j][k] -= factor * A[i][k]
        rank = sum(1 for row in A if any(val != 0 for val in row))
        return rank
    
    minimal_rank = gaussian_elimination(T_L)
    
    # Compute the width of the DPLL refutation tree
    def dpll_width(G):
        def is_satisfiable(clauses, assignment):
            for clause in clauses:
                if all(not var or (var > 0 and assignment[var - 1]) or (not var and not assignment[-var - 1]) for var in clause):
                    return True
            return False
        
        def dpll(clauses, assignment, level):
            if len(assignment) == n:
                return is_satisfiable(clauses, assignment)
            for var in range(1, n + 1):
                new_assignment = assignment[:]
                new_assignment.append(var > 0)
                if dpll(clauses, new_assignment, level + 1):
                    return True
                new_assignment[-1] = False
                if dpll(clauses, new_assignment, level + 1):
                    return True
            return False
        
        clauses = []
        for u in range(n):
            for v in range(u + 1, n):
                if G[u][v] != 0:
                    clauses.append([u + 1, -v - 1])
                    clauses.append([-u - 1, v + 1])
        
        return dpll(clauses, [], 0)
    
    w_DPLL = dpll_width(G)
    
    # Calculate the metric value
    if minimal_rank is None or w_DPLL == 0:
        return {
            "metric_name": "minimal_rank",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "DPLL width is zero"
        }
    
    metric_value = abs(minimal_rank) / w_DPLL
    
    # Check if the conjecture holds
    conjecture_holds = metric_value <= 2.0
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")