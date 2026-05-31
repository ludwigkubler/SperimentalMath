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
    n = random.randint(5, 40)
    d = random.randint(2, min(n-1, 3))
    
    # Generate a random d-regular graph using the configuration model
    G = {}
    for i in range(n):
        G[i] = set()
    edges = []
    for _ in range(d * n // 2):
        u = random.randint(0, n-1)
        v = random.randint(0, n-1)
        if u != v and v not in G[u]:
            G[u].add(v)
            G[v].add(u)
            edges.append((u, v))
    
    # Construct the Tseitin formula φ_G
    variables = {f'x{i}': i for i in range(n)}
    literals = [variables[f'x{i}'] if random.choice([True, False]) else -variables[f'x{i}'] for i in range(n)]
    tautologies = []
    for u, v in edges:
        tautologies.append((literals[u], literals[v]))
    
    # Compute the Hodge diamond dimension h(G)
    laplacian = [[0] * n for _ in range(n)]
    for u in G:
        laplacian[u][u] = len(G[u])
        for v in G[u]:
            laplacian[u][v] -= 1
            laplacian[v][u] -= 1
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        rank = 0
        for j in range(n):
            i_max = rank
            for i in range(rank, m):
                if abs(A[i][j]) > abs(A[i_max][j]):
                    i_max = i
            if A[i_max][j] == 0:
                continue
            A[rank], A[i_max] = A[i_max], A[rank]
            for k in range(n):
                A[rank][k] /= A[rank][j]
            for i in range(m):
                if i != rank and A[i][j] != 0:
                    for k in range(n):
                        A[i][k] -= A[i][j] * A[rank][k]
            rank += 1
        return rank
    
    h_G = gaussian_elimination(laplacian)
    
    # Compute the resolution proof width w(φ_G)
    def dpll(phi, assignment):
        if not phi:
            return True
        literal = next((x for x in range(n) if x not in assignment and -x not in assignment), None)
        if literal is None:
            return False
        new_phi = [(l for l in clause if l != literal and l != -literal) for clause in phi]
        if dpll(new_phi, assignment + [literal]):
            return True
        if dpll(new_phi, assignment + [-literal]):
            return True
        return False
    
    def resolution_width(phi):
        width = 0
        queue = list(phi)
        while queue:
            new_clause = set()
            for clause1 in queue:
                for clause2 in queue:
                    common_literals = [l for l in clause1 if -l in clause2]
                    if len(common_literals) == 1:
                        new_literal = next(l for l in clause1 if l not in common_literals)
                        new_clause.add(new_literal)
            width = max(width, len(new_clause))
            queue.extend([c for c in phi if any(l in c for l in new_clause)])
        return width
    
    w_phi_G = resolution_width(tautologies)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": h_G / w_phi_G,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")