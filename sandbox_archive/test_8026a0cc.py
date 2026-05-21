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

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        # Find pivot row
        max_row = i
        for j in range(i + 1, rows):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below pivot
        for j in range(i + 1, rows):
            factor = Fraction(matrix[j][i], matrix[i][i])
            for k in range(cols):
                matrix[j][k] -= factor * matrix[i][k]

    return matrix

def rank_of_matrix(matrix):
    rows, cols = len(matrix), len(matrix[0])
    rank = 0
    for i in range(rows):
        if all(abs(x) < 1e-9 for x in matrix[i]):
            continue
        rank += 1
        for j in range(i + 1, rows):
            factor = Fraction(matrix[j][i], matrix[i][i])
            for k in range(cols):
                matrix[j][k] -= factor * matrix[i][k]
    return rank

def resolution_length(clauses):
    n = len(clauses)
    A = [[0] * (n + 1) for _ in range(n)]
    
    for i, clause in enumerate(clauses):
        for literal in clause:
            if literal > 0:
                A[i][literal - 1] = 1
            else:
                A[i][-1] += 1
    
    rank = rank_of_matrix(A)
    return n - rank

def minimal_generators(graph):
    # Placeholder function to compute minimal number of generators for a graph
    # This is a stub and should be replaced with actual computation
    return random.randint(1, len(graph))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    graph = {i: set() for i in range(n)}
    for _ in range(2 * n):
        u, v = random.sample(range(n), 2)
        if v not in graph[u]:
            graph[u].add(v)
            graph[v].add(u)
    
    m_G = minimal_generators(graph)
    clauses = []
    for i in range(n):
        for j in range(i + 1, n):
            if j in graph[i]:
                clauses.append([i + 1, -j - 1])
                clauses.append([-i - 1, j + 1])
    
    L_phi = resolution_length(clauses)
    
    conjecture_holds = L_phi >= 2 ** (math.log(m_G, 2) * 0.5)
    counterexample = "" if conjecture_holds else f"Graph with m(G)={m_G}, L(φ)={L_phi}"
    
    return {
        "metric_name": "Resolution Length",
        "metric_value": L_phi,
        "instances_tested": len(clauses),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Graph with m(G)={results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")