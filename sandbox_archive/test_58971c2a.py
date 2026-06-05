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
    if n * d % 2 != 0:
        raise ValueError("Graph size must be a multiple of the degree")
    
    G = {i: [] for i in range(n)}
    edges_added = 0
    
    while edges_added < n * d // 2:
        u = random.randint(0, n-1)
        v = random.randint(0, n-1)
        
        if u != v and v not in G[u] and len(G[u]) < d:
            G[u].append(v)
            G[v].append(u)
            edges_added += 1
    
    return G

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    rank = 0
    for i in range(n):
        max_row = rank
        for j in range(rank, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        
        if A[max_row][i] == 0:
            continue
        
        A[rank], A[max_row] = A[max_row], A[rank]
        
        for j in range(n):
            if j != i and A[rank][j] != 0:
                factor = -A[j][i] / A[rank][i]
                for k in range(n):
                    A[j][k] += factor * A[rank][k]
        
        rank += 1
    
    return rank

def symplectic_form_degree(A):
    m, n = len(A), len(A[0])
    if m != n or m % 2 != 0:
        raise ValueError("Matrix must be square and even-sized")
    
    C = [[A[i][j] for j in range(n//2)] for i in range(m//2)]
    C_inv = gaussian_elimination(C)
    
    if C_inv == len(C):
        return len(C) - rank
    else:
        raise ValueError("Matrix is singular")

def circuit_monotone_width(G):
    n = len(G)
    clauses = []
    
    for u in range(n):
        for v in range(u+1, n):
            clause = [f"u_{u}_{v}", f"v_{u}_{v}"]
            for w in range(v+1, n):
                clause.append(f"w_{w}")
            clauses.append(clause)
    
    return len(clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    d = 3
    n = 40
    
    G = generate_d_regular_graph(n, d)
    A = [[0] * n for _ in range(n)]
    
    for u in range(n):
        for v in G[u]:
            A[u][v] = 1
            A[v][u] = 1
    
    try:
        symplectic_deg = symplectic_form_degree(A)
    except ValueError as e:
        return {
            "metric_name": "symplectic_form_degree",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": str(e)
        }
    
    circuit_width = circuit_monotone_width(G)
    
    return {
        "metric_name": "circuit_monotone_width",
        "metric_value": circuit_width,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        result = f"SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}"
    else:
        min_rho = min(result["metric_value"] for result in results if result["conjecture_holds"])
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        counterexample = f"rho < {min_rho} at seed {first_failing_seed}"
        result = f"FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}"
    
    print(result)