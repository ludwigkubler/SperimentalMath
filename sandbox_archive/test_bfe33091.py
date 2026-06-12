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

def generate_d_regular_graph(n, d):
    if n * d % 2 != 0:
        return None
    
    degree = [0] * n
    edges = []
    
    for v in range(n):
        while degree[v] < d:
            u = random.choice([u for u in range(n) if u != v and degree[u] < d])
            if (v, u) not in edges and (u, v) not in edges:
                edges.append((v, u))
                degree[v] += 1
                degree[u] += 1
    
    return edges

def tseitin_formula(edges):
    n = len(edges)
    literals = [f"x{i}" for i in range(n)]
    clauses = []
    
    for v, u in edges:
        clauses.append([f"~{literals[v]}", f"{literals[u]}"])
        clauses.append([f"~{literals[u]}", f"{literals[v]}"])
        clauses.append([f"{literals[v]}", f"{literals[u]}"])
    
    return literals, clauses

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i + 1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        
        # Swap rows
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below
        for j in range(i + 1, n):
            factor = matrix[j][i] / matrix[i][i]
            for k in range(n + 1):
                matrix[j][k] -= factor * matrix[i][k]
    
    return matrix

def minimal_local_index_of_sheaves(literals, clauses):
    n = len(literals)
    matrix = [[0] * (n + 1) for _ in range(n)]
    
    for clause in clauses:
        if len(clause) == 2 and clause[0].startswith('~') and clause[1].startswith('~'):
            u = int(clause[0][1:])
            v = int(clause[1][1:])
            matrix[u][v] += 1
            matrix[v][u] += 1
    
    matrix = gaussian_elimination(matrix)
    
    rank = sum(1 for row in matrix if any(x != 0 for x in row))
    return n - rank

def frege_proof_length(literals, clauses):
    # Simplified estimation of Frege proof length
    return len(clauses) * 2 + len(literals)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        d = 2
        G = generate_d_regular_graph(n, d)
        if G is None:
            continue
        
        literals, clauses = tseitin_formula(G)
        lrs = minimal_local_index_of_sheaves(literals, clauses)
        f_phi_G = frege_proof_length(literals, clauses)
        
        results.append((lrs, f_phi_G))
    
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    lrs_values = [r[0] for r in results]
    f_phi_G_values = [r[1] for r in results]
    
    mean_lrs = sum(lrs_values) / len(lrs_values)
    mean_f_phi_G = sum(f_phi_G_values) / len(f_phi_G_values)
    
    covariance = sum((lrs - mean_lrs) * (f_phi_G - mean_f_phi_G) for lrs, f_phi_G in results) / len(results)
    variance_lrs = sum((lrs - mean_lrs) ** 2 for lrs in lrs_values) / len(lrs_values)
    variance_f_phi_G = sum((f_phi_G - mean_f_phi_G) ** 2 for f_phi_G in f_phi_G_values) / len(f_phi_G_values)
    
    r = covariance / (math.sqrt(variance_lrs) * math.sqrt(variance_f_phi_G))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": r,
        "instances_tested": len(results),
        "n_max": max(len(literals) for literals, _ in results),
        "conjecture_holds": abs(r) >= 0.8 and abs(r) <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_r = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["metric_value"] is not None for r in results):
        RESULT = "SUPPORTED" if support_fraction >= 0.8 else "FALSIFIED"
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        RESULT = f"FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}"
    else:
        RESULT = "INCONCLUSIVE"
    
    print(f"RESULT: {RESULT} mean={mean_r:.2f} support_fraction={support_fraction:.2f}")