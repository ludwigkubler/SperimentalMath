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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def solve_linear_system(A, b):
    n = len(A)
    A_b = [row + [b[i]] for i, row in enumerate(A)]
    A_b = gaussian_elimination(A_b)
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (A_b[i][-1] - sum(A_b[i][j] * x[j] for j in range(i + 1, n))) / A_b[i][i]
    return x

def is_integer(x):
    return abs(x - round(x)) < 1e-9

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_random_graph(n):
        G = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    G[i][j] = G[j][i] = 1
        return G
    
    def clique_complex_betti_numbers(G):
        n = len(G)
        betti_0 = 1  # Connected components
        betti_1 = sum(1 for i in range(n) for j in range(i + 1, n) if G[i][j] == 1)
        return betti_0, betti_1
    
    def max_cut_approximation(G):
        n = len(G)
        A = [[0] * (n + 2) for _ in range(n + 2)]
        b = [0] * (n + 2)
        c = [0] * (n + 2)
        
        for i in range(n):
            for j in range(i + 1, n):
                if G[i][j]:
                    A[i][i], A[j][j], A[n][n], A[n + 1][n + 1] = 1, 1, -1, -1
                    A[i][n + 1], A[j][n], A[n][i], A[n + 1][j] = -1, -1, 1, 1
                    b[i], b[j], b[n], b[n + 1] = 0, 0, 1, 1
        
        x = solve_linear_system(A, b)
        return sum(x[i] for i in range(n) if x[i] > 0.5)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        G = generate_random_graph(n)
        betti_0, betti_1 = clique_complex_betti_numbers(G)
        required_degree = max_cut_approximation(G)
        
        if not is_integer(required_degree):
            return {
                "metric_name": "SOS Degree",
                "metric_value": float('nan'),
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": "Non-integer degree"
            }
        
        results.append((n, required_degree, betti_0 + betti_1))
    
    total_required = sum(required for _, required, _ in results)
    total_betti_sum = sum(betti for _, _, betti in results)
    average_required = total_required / len(results)
    average_betti_sum = total_betti_sum / len(results)
    
    return {
        "metric_name": "SOS Degree",
        "metric_value": average_required,
        "instances_tested": len(results),
        "conjecture_holds": average_required >= average_betti_sum,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean = sum(r['metric_value'] for r in results) / len(results)
    std = math.sqrt(sum((r['metric_value'] - mean) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")