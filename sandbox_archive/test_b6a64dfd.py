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
    
    def generate_max_cut_instance(n):
        G = {}
        for i in range(n):
            G[i] = set()
        edges = [(i, j) for i in range(n) for j in range(i+1, n)]
        random.shuffle(edges)
        m = len(edges)
        for u, v in edges[:m//2]:
            G[u].add(v)
            G[v].add(u)
        return G
    
    def degree(G, v):
        return len(G[v])
    
    def laplacian_matrix(G, n):
        L = [[0] * n for _ in range(n)]
        for i in range(n):
            deg_i = degree(G, i)
            L[i][i] = deg_i
            for j in G[i]:
                L[i][j] = -1
                L[j][i] = -1
        return L
    
    def eigenvalues(M):
        n = len(M)
        if n == 0:
            return []
        if n == 1:
            return [M[0][0]]
        
        # Gaussian elimination to find eigenvalues
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(M[j][i]) > abs(M[max_row][i]):
                    max_row = j
            M[i], M[max_row] = M[max_row], M[i]
            
            factor = 1 / M[i][i]
            for j in range(n):
                M[i][j] *= factor
            
            for j in range(i+1, n):
                factor = M[j][i]
                for k in range(n):
                    M[j][k] -= factor * M[i][k]
        
        return [M[i][i] for i in range(n)]
    
    def sos_moment_matrix(G, d):
        n = len(G)
        M_d = [[0] * (n + 1) for _ in range(n + 1)]
        for v in G:
            deg_v = degree(G, v)
            M_d[v][v] += deg_v
            for u in G[v]:
                M_d[u][u] += 1
                M_d[v][u] -= 1
                M_d[u][v] -= 1
        
        # Add identity matrix to make it positive semi-definite
        for i in range(n):
            M_d[i][i] += 1
        
        return M_d
    
    n = random.randint(5, 40)
    G = generate_max_cut_instance(n)
    
    integrality_gap = 0.878 / (n - 1)
    
    results = []
    for d in [2, 3, 4]:
        M_d = sos_moment_matrix(G, d)
        eigenvals = eigenvalues(M_d)
        lambda_min = min(eigenvals)
        
        if lambda_min >= integrality_gap:
            gap = 0
        else:
            gap = 1 - lambda_min
        
        results.append({
            "d": d,
            "lambda_min": lambda_min,
            "gap": gap
        })
    
    metric_value = sum(r["gap"] for r in results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(r["gap"] <= 1 - integrality_gap for r in results)
    counterexample = "" if conjecture_holds else "Integrality gap exceeds 0.878"
    
    return {
        "metric_name": "Integrality Gap",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Integrality gap exceeds 0.878' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")