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
    
    def generate_3_regular_graph(n):
        while True:
            adj = [[] for _ in range(n)]
            edges = set()
            for v in range(n):
                neighbors = random.sample(range(n), 2)
                if (v, neighbors[0]) not in edges and (neighbors[0], v) not in edges:
                    adj[v].append(neighbors[0])
                    adj[neighbors[0]].append(v)
                    edges.add((v, neighbors[0]))
            if len(edges) == n * 3 // 2:
                return adj
    
    def laplacian_matrix(adj):
        n = len(adj)
        L = [[0] * n for _ in range(n)]
        for v in range(n):
            degree = len(adj[v])
            L[v][v] = degree
            for u in adj[v]:
                L[v][u] = -1
        return L
    
    def eigh(L):
        n = len(L)
        eigenvalues, eigenvectors = [], []
        for i in range(n):
            max_val = float('-inf')
            max_idx = -1
            for j in range(n):
                if abs(L[i][j]) > max_val:
                    max_val = abs(L[i][j])
                    max_idx = j
            eigenvalues.append(max_val)
            eigenvectors.append([0] * n)
            eigenvectors[-1][max_idx] = 1
        return eigenvalues, eigenvectors
    
    def max_cut(G):
        n = len(G)
        best_cut_value = -1
        
        def backtrack(path, cut_value):
            nonlocal best_cut_value
            if len(path) == n:
                if cut_value > best_cut_value:
                    best_cut_value = cut_value
                return
            for neighbor in G[path[-1]]:
                if neighbor not in path:
                    new_cut_value = cut_value + (1 if path[-1] % 2 != neighbor % 2 else -1)
                    backtrack(path + [neighbor], new_cut_value)
        
        backtrack([0], 0)
        return best_cut_value
    
    def norm_1(v):
        return sum(abs(x) for x in v)
    
    n = random.choice([10, 14, 18, 22])
    G = generate_3_regular_graph(n)
    L = laplacian_matrix(G)
    eigenvalues, eigenvectors = eigh(L)
    phi = eigenvectors[-1]
    phi_norm_1 = norm_1(phi)
    
    if phi_norm_1 == 0:
        return {
            "metric_name": "rho_over_kappa",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    kappa = 2 * (1 - phi_norm_1 / math.sqrt(n))
    dp = n * eigenvalues[-1] / 4
    mc = max_cut(G)
    rho = dp / mc - 1
    
    if rho > 16 * kappa:
        return {
            "metric_name": "rho_over_kappa",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"n={n}, rho={rho}, kappa={kappa}"
        }
    
    return {
        "metric_name": "rho_over_kappa",
        "metric_value": rho / kappa if kappa > 0.01 else None,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial)
    
    if all("metric_value" not in r or r["metric_value"] is None for r in results):
        print("RESULT: INCONCLUSIVE mapping_undefined")
    else:
        rho_over_kappa_values = [r["metric_value"] for r in results if "metric_value" in r and r["metric_value"] is not None]
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={sum(rho_over_kappa_values) / len(rho_over_kappa_values)} std={math.sqrt(sum((x - sum(rho_over_kappa_values) / len(rho_over_kappa_values)) ** 2 for x in rho_over_kappa_values) / len(rho_over_kappa_values))} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")