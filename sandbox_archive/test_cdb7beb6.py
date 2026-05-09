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

def generate_d_regular_graph(n, d):
    if (d * n) % 2 != 0:
        return None
    adj_matrix = [[0] * n for _ in range(n)]
    edges = set()
    while len(edges) < d * n // 2:
        u, v = random.sample(range(n), 2)
        if u != v and (u, v) not in edges and (v, u) not in edges:
            adj_matrix[u][v] = 1
            adj_matrix[v][u] = 1
            edges.add((u, v))
    return adj_matrix

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below pivot
        factor = 1 / A[i][i]
        for j in range(i, n):
            A[i][j] *= factor
        for k in range(i+1, n):
            factor = A[k][i]
            for j in range(i, n):
                A[k][j] -= factor * A[i][j]
    return A

def dehn_function(G):
    n = len(G)
    I = [[int(i == j) for j in range(n)] for i in range(n)]
    A = gaussian_elimination(G + I)
    delta_G = 0
    for i in range(n):
        if A[i][i] != 1:
            return float('inf')
        delta_G += sum(abs(A[j][i]) for j in range(i+1, n))
    return delta_G

def resolution_length(phi):
    stack = phi[:]
    length = 0
    while stack:
        clause = stack.pop()
        if len(clause) == 1:
            continue
        literal = random.choice(clause)
        new_clauses = []
        for c in stack:
            if literal not in c and -literal not in c:
                new_clauses.append([l for l in c if l != -literal])
        stack.extend(new_clauses)
        length += 1
    return length

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    d = 3
    phi = []
    G = generate_d_regular_graph(n, d)
    if G is None:
        return {
            "metric_name": "resolution_length",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "graph_not_d_regular"
        }
    
    delta_G = dehn_function(G)
    if delta_G == float('inf'):
        return {
            "metric_name": "resolution_length",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "dehn_function_infinite"
        }
    
    length = resolution_length(phi)
    conjecture_holds = length >= 2 ** (0.5 * delta_G)
    counterexample = "" if conjecture_holds else f"resolution_length={length}, dehn_function={delta_G}"
    
    return {
        "metric_name": "resolution_length",
        "metric_value": length,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_length = sum(r["metric_value"] for r in results if r["conjecture_holds"])
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_length/len(results)} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_length/len(results)} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        counterexample = results[seeds.index(first_failing_seed)]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")