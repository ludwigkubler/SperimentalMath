# auto-injected by SEC sandbox
import math
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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a*b) // gcd(a, b)

def matrix_multiply(A, B):
    m, k = len(A), len(B)
    n = len(B[0])
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for l in range(k):
                C[i][j] += A[i][l] * B[l][j]
    return C

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    augmented_matrix = [A[i] + [b[i]] for i in range(m)]
    for i in range(n):
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

def matrix_inverse(A):
    m, n = len(A), len(A[0])
    identity = [[Fraction(1 if i == j else 0) for j in range(n)] for i in range(m)]
    augmented_matrix = A + identity
    for i in range(n):
        max_row = i
        for j in range(i+1, m):
            if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                max_row = j
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        pivot = augmented_matrix[i][i]
        for j in range(i, n*2):
            augmented_matrix[i][j] /= pivot
        for j in range(m):
            if j != i:
                factor = augmented_matrix[j][i]
                for k in range(i, n*2):
                    augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
    return [row[n:] for row in augmented_matrix]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        if n > 40:
            return {
                "metric_name": "Coxeter Group Rank Bound on Communication Complexity Rank Variance",
                "metric_value": None,
                "instances_tested": 0,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "budget_exceeded"
            }
        for _ in range(5):
            # Generate a random circuit
            vertices = list(range(n))
            edges = []
            for u in vertices:
                for v in vertices:
                    if u != v and random.random() < 0.1:
                        edges.append((u, v))
            
            # Construct the associated Coxeter group G(C)
            generators = set()
            relations = set()
            for u, v in edges:
                generators.add(u)
                generators.add(v)
                d = abs(u - v) % n
                if d not in relations:
                    relations.add(d)
            
            # Compute the rank of G(C)
            G_C_rank = len(generators)
            
            # Compute the communication complexity rank r(C)
            r_C = len(edges)
            
            # Check the conjecture
            if G_C_rank > 1.44 * r_C**2:
                return {
                    "metric_name": "Coxeter Group Rank Bound on Communication Complexity Rank Variance",
                    "metric_value": None,
                    "instances_tested": 0,
                    "n_max": n,
                    "conjecture_holds": False,
                    "counterexample": f"Counterexample found for n={n}, G(C) rank={G_C_rank}, r(C)={r_C}"
                }
            
            results.append((G_C_rank, r_C))
    
    # Compute the mean and std of metric_value
    if not results:
        return {
            "metric_name": "Coxeter Group Rank Bound on Communication Complexity Rank Variance",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "No results collected"
        }
    
    mean = sum(result[0] - result[1]**2 for result in results) / len(results)
    std = (sum((result[0] - result[1]**2 - mean)**2 for result in results) / len(results))**0.5
    
    # Check the acceptance criterion
    support_fraction = sum(1 for result in results if abs(result[0] - result[1]**2) <= 0.5) / len(results)
    
    return {
        "metric_name": "Coxeter Group Rank Bound on Communication Complexity Rank Variance",
        "metric_value": mean,
        "instances_tested": len(results),
        "n_max": 40,
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std = (sum((r["metric_value"] - mean)**2 for r in results if r["metric_value"] is not None) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"First failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE No seeds supported the conjecture")