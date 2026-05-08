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
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]

def matrix_multiply(A, B):
    m, n = len(A), len(B[0])
    p = len(B)
    C = [[0 for _ in range(n)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 40
    G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        G[i][i] = 0
    
    # Construct resolution graph
    resolution_graph = []
    for i in range(n):
        for j in range(i+1, n):
            if G[i][j]:
                resolution_graph.append((i, j))
    
    # Compute persistent homology (simplified version)
    max_persistence = 0
    for edge in resolution_graph:
        A = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            if i != edge[0] and i != edge[1]:
                A[i][i] = 1
        gaussian_elimination(A)
        rank = sum(1 for row in A if any(row))
        persistence = n - rank
        max_persistence = max(max_persistence, persistence)
    
    # Estimate resolution proof size (simplified DPLL-based estimation)
    def dpll_size(G):
        if not G:
            return 0
        if all(sum(row) == 1 for row in G):
            return len(G)
        for i in range(len(G)):
            if sum(G[i]) > 1:
                new_G = [row[:] for row in G]
                new_G.pop(i)
                return 1 + dpll_size(new_G)
        return float('inf')
    
    size_of_proof = dpll_size(resolution_graph)
    
    # Check conjecture
    if size_of_proof == float('inf'):
        return {
            "metric_name": "max_persistence",
            "metric_value": max_persistence,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    conjecture_holds = max_persistence >= math.log2(size_of_proof) / n
    counterexample = "" if conjecture_holds else f"max_persistence={max_persistence}, size_of_proof={size_of_proof}"
    
    return {
        "metric_name": "max_persistence",
        "metric_value": max_persistence,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]]
    if not seeds:
        from sympy import primerange
        seeds = list(primerange(2, 200))[:30]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")