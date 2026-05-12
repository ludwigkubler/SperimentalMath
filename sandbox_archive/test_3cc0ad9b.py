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

def matrix_mult(A, B):
    m = len(A)
    n = len(B[0])
    p = len(B)
    C = [[0 for _ in range(n)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    n = len(A)
    M = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(M[j][i]) > abs(M[max_row][i]):
                max_row = j
        M[i], M[max_row] = M[max_row], M[i]
        factor = M[i][i]
        for j in range(i, n + 1):
            M[i][j] /= factor
        for j in range(n):
            if j != i:
                factor = M[j][i]
                for k in range(i, n + 1):
                    M[j][k] -= factor * M[i][k]
    x = [M[i][-1] for i in range(n)]
    return x

def det(A):
    n = len(A)
    if n == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]
    det_val = 0
    for c in range(n):
        sub_matrix = [row[:c] + row[c+1:] for row in A[1:]]
        sign = (-1) ** (c % 2)
        sub_det = det(sub_matrix)
        det_val += sign * A[0][c] * sub_det
    return det_val

def euler_characteristic(clique_complex):
    n = len(clique_complex)
    return sum((-1)**k * len([c for c in clique_complex if len(c) == k]) for k in range(n + 1))

def communication_graph(f, n):
    vertices = [(i, j) for i in range(2**n) for j in range(i+1, 2**n)]
    edges = []
    for u, v in vertices:
        if f(u) != f(v):
            edges.append((u, v))
    return vertices, edges

def clique_complex(vertices, edges):
    n = len(vertices)
    cliques = [set([i]) for i in range(n)]
    for edge in edges:
        u, v = edge
        new_cliques = set()
        for c in cliques:
            if u in c and v not in c:
                new_cliques.add(c | {v})
            elif v in c and u not in c:
                new_cliques.add(c | {u})
            else:
                new_cliques.add(c)
        cliques.update(new_cliques)
    return [c for c in cliques if len(c) > 1]

def deterministic_communication_complexity(f, n):
    vertices = [(i, j) for i in range(2**n) for j in range(i+1, 2**n)]
    edges = []
    for u, v in vertices:
        if f(u) != f(v):
            edges.append((u, v))
    G = {v: set() for v in vertices}
    for u, v in edges:
        G[u].add(v)
        G[v].add(u)
    visited = [False] * len(vertices)
    def dfs(node):
        stack = [node]
        while stack:
            node = stack.pop()
            if not visited[node]:
                visited[node] = True
                for neighbor in G[node]:
                    stack.append(neighbor)
    dfs(0)
    return sum(1 for v in range(len(vertices)) if visited[v])

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 5 + (seed % 6) * 5
    f = lambda x: sum(x[i] & x[j] for i in range(n) for j in range(i+1, n)) % 2
    vertices, edges = communication_graph(f, n)
    clique_complex_ = clique_complex(vertices, edges)
    euler_char = euler_characteristic(clique_complex_)
    comm_complexity = deterministic_communication_complexity(f, n)
    diff = abs(euler_char - comm_complexity)
    return {
        "metric_name": "Absolute Difference",
        "metric_value": diff,
        "instances_tested": 1,
        "conjecture_holds": diff == 0,
        "counterexample": "" if diff == 0 else f"Counterexample for n={n}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_diff = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_diff)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_diff} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='First failing seed' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")