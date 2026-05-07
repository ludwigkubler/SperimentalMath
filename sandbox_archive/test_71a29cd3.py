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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_multiply(A, B):
    m, k, n = len(A), len(B), len(B[0])
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for l in range(k):
                C[i][j] += A[i][l] * B[l][j]
    return C

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    augmented = [A[i] + [b[i]] for i in range(m)]
    for i in range(n):
        max_row = i
        for j in range(i+1, m):
            if abs(augmented[j][i]) > abs(augmented[max_row][i]):
                max_row = j
        augmented[i], augmented[max_row] = augmented[max_row], augmented[i]
        pivot = augmented[i][i]
        for j in range(n + 1):
            augmented[i][j] /= pivot
        for j in range(m):
            if j != i:
                factor = augmented[j][i]
                for k in range(n + 1):
                    augmented[j][k] -= factor * augmented[i][k]
    return [row[-1] for row in augmented]

def rank(A):
    m, n = len(A), len(A[0])
    A_copy = [row[:] for row in A]
    return len(gaussian_elimination(A_copy, [0]*n))

def is_clique(G, vertices):
    for u in vertices:
        for v in vertices:
            if u != v and (u, v) not in G and (v, u) not in G:
                return False
    return True

def generate_k_clique_instance(n, k):
    G = {}
    vertices = list(range(n))
    random.shuffle(vertices)
    selected_vertices = vertices[:k]
    for i in range(k):
        for j in range(i+1, k):
            G[(selected_vertices[i], selected_vertices[j])] = True
            G[(selected_vertices[j], selected_vertices[i])] = True
    return G

def generate_random_instance(n):
    G = {}
    vertices = list(range(n))
    random.shuffle(vertices)
    for u in vertices:
        for v in range(u+1, n):
            if random.choice([True, False]):
                G[(u, v)] = True
                G[(v, u)] = True
    return G

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        k = math.ceil(n ** (1/3))
        G = generate_k_clique_instance(n, k)
        
        # Construct polymatroid via clause incidence matrix
        A = [[0] * n for _ in range(k)]
        for i in range(k):
            for j in range(n):
                if (i, j) in G:
                    A[i][j] = 1
        
        rank_k_clique = rank(A)
        
        # Check ρ ≥ n^{1/2}·k^{1/4}
        lower_bound = math.sqrt(n) * k ** (1/4)
        if rank_k_clique < lower_bound:
            results.append({
                "n": n,
                "k": k,
                "rank": rank_k_clique,
                "lower_bound": lower_bound,
                "conjecture_holds": False,
                "counterexample": f"Rank {rank_k_clique} < {lower_bound}"
            })
        else:
            results.append({
                "n": n,
                "k": k,
                "rank": rank_k_clique,
                "lower_bound": lower_bound,
                "conjecture_holds": True,
                "counterexample": ""
            })
    
    # Check against DNF formulas with size ≤ n^2 (using subset lattice polymatroids)
    for n in n_values:
        k = math.ceil(n ** (1/3))
        G = generate_random_instance(n)
        
        # Construct polymatroid via clause incidence matrix
        A = [[0] * n for _ in range(2**n)]
        for i in range(2**n):
            for j in range(n):
                if bin(i)[2:].zfill(n)[j] == '1':
                    A[i][j] = 1
        
        rank_dnf = rank(A)
        
        # Check ρ ≤ log n + 2 log k
        upper_bound = math.log(n) + 2 * math.log(k)
        if rank_dnf > upper_bound:
            results.append({
                "n": n,
                "k": k,
                "rank": rank_dnf,
                "upper_bound": upper_bound,
                "conjecture_holds": False,
                "counterexample": f"Rank {rank_dnf} > {upper_bound}"
            })
        else:
            results.append({
                "n": n,
                "k": k,
                "rank": rank_dnf,
                "upper_bound": upper_bound,
                "conjecture_holds": True,
                "counterexample": ""
            })
    
    metric_values = [result["rank"] for result in results]
    conjecture_holds = all(result["conjecture_holds"] for result in results)
    counterexample = next((result["counterexample"] for result in results if not result["conjecture_holds"]), "")
    
    return {
        "metric_name": "polymatroid_rank",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")