# auto-injected by SEC sandbox
import collections
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
import json
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_truth_table(k):
        return [random.choice([0, 1]) for _ in range(2**k)]
    
    def is_minimal_1_certificate(f, C):
        for i in range(len(C)):
            if f[C[:i] + (1 - C[i],) + C[i+1:]] == f[C]:
                return False
        return True
    
    def build_conflict_graph(f, k):
        vertices = [C for C in combinations(range(k), len(C)) if is_minimal_1_certificate(f, C)]
        edges = []
        for C, C_prime in combinations(vertices, 2):
            common_vars = set(i for i in range(k) if C[i] != C_prime[i])
            if any(f[C[:i] + (1 - C[i],) + C[i+1:]] != f[C_prime[:i] + (1 - C_prime[i],) + C_prime[i+1:]] for i in common_vars):
                edges.append((C, C_prime))
        return vertices, edges
    
    def laplacian_matrix(G):
        n = len(G[0])
        L = [[0] * n for _ in range(n)]
        for i in range(n):
            degree = sum(1 for j in range(n) if G[0][i] == G[0][j])
            L[i][i] = -degree
            for j in range(i + 1, n):
                if (G[0][i], G[0][j]) in G[1]:
                    L[i][j] = L[j][i] = 1
        return L
    
    def determinant(M):
        n = len(M)
        det = 0
        for i in range(n):
            submatrix = [row[:i] + row[i+1:] for row in M[1:]]
            sign = (-1) ** i
            if n == 2:
                det += sign * M[0][i] * M[1][1]
            else:
                det += sign * M[0][i] * determinant(submatrix)
        return det
    
    def Q_dt(f, k):
        memo = {}
        
        def dp(mask):
            if mask in memo:
                return memo[mask]
            if len(mask) == 1:
                return 1
            max_val = -math.inf
            for i in range(len(mask)):
                new_mask = tuple(0 if j == i else mask[j] for j in range(len(mask)))
                max_val = max(max_val, dp(new_mask))
            memo[mask] = max_val
            return max_val
        
        return dp(tuple(range(k)))
    
    def minmax_dp(f, k):
        memo = {}
        
        def dp(mask):
            if mask in memo:
                return memo[mask]
            if len(mask) == 1:
                return 0
            min_val = math.inf
            for i in range(len(mask)):
                new_mask = tuple(0 if j == i else mask[j] for j in range(len(mask)))
                min_val = min(min_val, dp(new_mask))
            memo[mask] = min_val
            return min_val
        
        return dp(tuple(range(k)))
    
    def log2(x):
        return math.log2(x)
    
    k_values = [3, 4, 5, 6]
    results = []
    for k in k_values:
        for _ in range(200):
            f = generate_truth_table(k)
            C = list(range(k))
            if not is_minimal_1_certificate(f, C):
                continue
            vertices, edges = build_conflict_graph(f, k)
            L = laplacian_matrix((vertices, edges))
            tau_G_f = determinant(L)
            Q_dt_f = Q_dt(f, k)
            minmax_dp_f = minmax_dp(f, k)
            delta = log2(tau_G_f) - Q_dt_f * log2(k + 1)
            results.append(delta)
    
    mean_delta = sum(results) / len(results)
    conjecture_holds = all(delta <= 0 for delta in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "delta",
        "metric_value": mean_delta,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps(result)}")
        results.append(result)
    
    mean_delta = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_delta} std=0.0 support_fraction={support_fraction}")
    elif any(r["delta"] > 1e-9 for r in results):
        first_failing_seed = next(r["seed"] for r in results if r["delta"] > 1e-9)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE mapping_undefined")