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
from fractions import Fraction
from math import sqrt, log2

def generate_d_regular_graph(n: int, d: int) -> list:
    if 2 * d > n or n % 2 != 0:
        return None  # Cannot form a d-regular graph with these parameters
    
    G = [[] for _ in range(n)]
    available_neighbors = set(range(1, n))
    
    for i in range(d):
        for j in range(i + 1, n):
            if len(G[i]) < d and len(G[j]) < d:
                G[i].append(j)
                G[j].append(i)
                available_neighbors.discard(j)
    
    return G

def hodge_decomposition_complexity(G: list) -> float:
    n = len(G)
    A = [[0] * n for _ in range(n)]
    
    # Construct the adjacency matrix
    for i in range(n):
        for j in G[i]:
            A[i][j] = 1
    
    # Compute the Laplacian matrix L = D - A
    D = [[0] * n for _ in range(n)]
    for i in range(n):
        D[i][i] = sum(A[i])
    
    L = [[D[i][j] - A[i][j] for j in range(n)] for i in range(n)]
    
    # Compute the eigenvalues of L
    eigenvalues = []
    for k in range(n):
        if all(L[k][k] == 0 for _ in range(k)):
            eigenvalue = 0
        else:
            u = [1] * n
            v = [L[i][k] / L[k][k] for i in range(n)]
            while sum(u) != 0:
                u = [v[i] - (sum(v[j]) * u[j]) / sum(u[j]) for j in range(n)]
                v = [u[i] - (sum(u[j]) * v[j]) / sum(v[j]) for j in range(n)]
            eigenvalue = abs(sum(u) / n)
        eigenvalues.append(eigenvalue)
    
    # The Hodge decomposition complexity is the sum of the eigenvalues
    return sum(eigenvalues)

def resolution_proof_width(G: list) -> int:
    n = len(G)
    clauses = []
    
    for i in range(n):
        clause = [i + 1]
        for j in G[i]:
            clause.append(-(j + 1))
        clauses.append(clause)
    
    # Convert to Tseitin formula
    tseitin_vars = {}
    tseitin_count = 0
    
    def add_clause(clause):
        nonlocal tseitin_count
        tseitin_count += 1
        tseitin_vars[tseitin_count] = clause
    
    for i in range(n):
        add_clause([i + 1, -(tseitin_count + 1)])
        add_clause([-i - 1, tseitin_count + 1])
    
    for i in range(n):
        for j in G[i]:
            add_clause([-(i + 1), -(j + 1), tseitin_count + 2])
            add_clause([i + 1, j + 1, -(tseitin_count + 2)])
            add_clause([-i - 1, -(j + 1), -(tseitin_count + 2)])
            add_clause([i + 1, -(j + 1), tseitin_count + 3])
            add_clause([-i - 1, j + 1, tseitin_count + 3])
    
    # Compute the width of the resolution proof
    queue = []
    for clause in clauses:
        queue.append(clause)
    
    while queue:
        literal = random.choice(queue[0])
        if literal > 0:
            literal = -literal
        
        new_clauses = []
        for clause in queue:
            if literal not in clause and -literal not in clause:
                new_clauses.append([l for l in clause if l != -literal])
        
        queue = new_clauses
    
    return tseitin_count

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 40
    d = 3
    G = generate_d_regular_graph(n, d)
    
    if G is None:
        return {
            "metric_name": "Hodge Decomposition Complexity",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    hd_G = hodge_decomposition_complexity(G)
    w_phi_G = resolution_proof_width(G)
    
    return {
        "metric_name": "Hodge Decomposition Complexity",
        "metric_value": hd_G,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(hd_G - w_phi_G) <= 3,
        "counterexample": "" if abs(hd_G - w_phi_G) <= 3 else f"hd(G)={hd_G}, w(φ_G)={w_phi_G}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.2f} std={sqrt(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values) / len(metric_values)):.2f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")