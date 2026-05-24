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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            if pivot == 0:
                continue
            for j in range(n):
                A[i][j] /= pivot
            for k in range(m):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def tropical_add(a, b):
        return max(a, b)

    def tropical_multiply(a, b):
        if a == float('-inf') or b == float('-inf'):
            return float('-inf')
        return a + b

    def tropical_power_series_rank(n):
        # Generate a random satisfiable instance of max-CUT
        G = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if random.random() < 0.5:
                    G[i][j] = G[j][i] = random.randint(1, 10)
        
        # Compute the DPLL refutation tree diameter
        def dpll(G, assignment, path):
            if len(path) > 2 * n:
                return 0
            if all(G[i][j] == 0 for i in range(n) for j in range(i+1, n)):
                return len(path)
            max_diameter = 0
            for v in range(n):
                if assignment[v] is None:
                    new_assignment = assignment[:]
                    new_assignment[v] = True
                    diameter_true = dpll(G, new_assignment, path + [v])
                    new_assignment[v] = False
                    diameter_false = dpll(G, new_assignment, path + [v])
                    max_diameter = max(max_diameter, diameter_true, diameter_false)
            return max_diameter
        
        assignment = [None] * n
        diameter = dpll(G, assignment, [])
        
        # Compute the minimal rank of the tropical power series
        A = [[tropical_add(-float('inf'), G[i][j]) for j in range(n)] for i in range(n)]
        rank = 0
        while any(any(row) for row in A):
            rank += 1
            A = gaussian_elimination(A)
        
        return rank, diameter

    n = random.randint(5, 40)
    rank, diameter = tropical_power_series_rank(n)
    
    metric_value = rank / (2 * diameter)
    conjecture_holds = rank >= 2 * diameter
    counterexample = "" if conjecture_holds else f"n={n}, rank={rank}, diameter={diameter}"
    
    return {
        "metric_name": "tropical_power_series_rank",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.4f} std={std_metric_value:.4f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")