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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def tseitin_formula(graph):
        n = len(graph)
        literals = [random.randint(1, 2*n) for _ in range(n)]
        clauses = []
        for i in range(n):
            clauses.append([literals[2*i], -literals[2*i+1]])
        for u in range(n):
            for v in range(u+1, n):
                if graph[u][v]:
                    literals_u = [literals[2*u], -literals[2*u+1]]
                    literals_v = [literals[2*v], -literals[2*v+1]]
                    clauses.append([-literals_u[0], -literals_v[0]])
                    clauses.append([-literals_u[0], literals_v[1]])
                    clauses.append([literals_u[1], -literals_v[0]])
                    clauses.append([literals_u[1], literals_v[1]])
        return literals, clauses
    
    def resolution_length(clauses):
        unit_clauses = [c for c in clauses if len(c) == 1]
        while True:
            new_unit_clauses = []
            for i in range(len(unit_clauses)):
                for j in range(i+1, len(unit_clauses)):
                    lit_i, = unit_clauses[i]
                    lit_j, = unit_clauses[j]
                    if -lit_i in clauses and -lit_j in clauses:
                        new_clause = [l for l in clauses if l != [-lit_i] and l != [-lit_j]]
                        if len(new_clause) == 0:
                            return len(unit_clauses)
                        new_unit_clauses.append([l for l in new_clause if len(l) == 1])
            unit_clauses.extend(new_unit_clauses)
    
    def generate_random_graph(n, p):
        graph = [[False] * n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if random.random() < p:
                    graph[i][j] = True
                    graph[j][i] = True
        return graph
    
    def asymptotic_dimension(graph):
        n = len(graph)
        max_radius = 0
        for v in range(n):
            radius = 0
            visited = [False] * n
            queue = [(v, 0)]
            while queue:
                u, dist = queue.pop(0)
                if not visited[u]:
                    visited[u] = True
                    radius = max(radius, dist)
                    for w in range(n):
                        if graph[u][w] and not visited[w]:
                            queue.append((w, dist + 1))
            max_radius = max(max_radius, radius)
        return math.ceil(math.log2(max_radius + 1))
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    p = 0.5
    graph = generate_random_graph(n, p)
    d = asymptotic_dimension(graph)
    literals, clauses = tseitin_formula(graph)
    length = resolution_length(clauses)
    
    return {
        "metric_name": "resolution_length",
        "metric_value": length,
        "instances_tested": 1,
        "conjecture_holds": length >= 2 ** (d - 1),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_length = sum(r["metric_value"] for r in results) / len(results)
    std_length = math.sqrt(sum((r["metric_value"] - mean_length) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_length} std={std_length} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"asymptotic_dimension\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")