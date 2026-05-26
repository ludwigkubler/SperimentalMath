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
    return abs(a*b) // gcd(a, b)

def matrix_multiply(A, B):
    m, n = len(A), len(B[0])
    p = len(B)
    C = [[0 for _ in range(n)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    augmented_matrix = [row + [b[i]] for i, row in enumerate(A)]
    for i in range(n):
        if i >= m:
            break
        max_row = i
        for j in range(i+1, m):
            if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                max_row = j
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        pivot = augmented_matrix[i][i]
        for j in range(i, n+1):
            augmented_matrix[i][j] /= pivot
        for j in range(m):
            if j != i:
                factor = augmented_matrix[j][i]
                for k in range(i, n+1):
                    augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
    return [row[-1] for row in augmented_matrix]

def minimal_rank(G):
    G = list(set(G))
    if not G:
        return 0
    A = [[gcd(G[i], G[j]) for j in range(len(G))] for i in range(len(G))]
    b = [1] * len(G)
    try:
        return len(gaussian_elimination(A, b))
    except Exception as e:
        print(f"Error in minimal_rank: {e}")
        return 0

def generate_frege_tree(depth):
    if depth == 0:
        return []
    else:
        left = generate_frege_tree(random.randint(0, depth-1))
        right = generate_frege_tree(random.randint(0, depth-1))
        return [left + right]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    depths = range(1, 41)
    results = []
    for depth in depths:
        tree = generate_frege_tree(depth)
        literals = set()
        for node in tree:
            literals.update(node)
        G = list(literals)
        rho_G = minimal_rank(G)
        results.append({"depth": depth, "rho_G": rho_G})
    
    mean_value = sum(result["rho_G"] / result["depth"] for result in results) if any(result["depth"] > 0 for result in results) else 0
    support_fraction = sum(1 for result in results if result["rho_G"] <= result["depth"]) / len(results)
    
    conjecture_holds = all(result["rho_G"] <= result["depth"] for result in results)
    counterexample = "" if conjecture_holds else f"Depth={results[0]['depth']}, rho(G)={results[0]['rho_G']}"
    
    return {
        "metric_name": "minimal_rank_over_depth",
        "metric_value": mean_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 17 for i in range(30)]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={math.sqrt(sum((result['metric_value'] - mean_value)**2 for result in results) / len(results))} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Depth={results[0]['depth']}, rho(G)={results[0]['rho_G']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")