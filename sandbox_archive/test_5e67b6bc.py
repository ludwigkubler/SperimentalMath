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
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_k_regular_graph(n, k):
        if (k * n) % 2 != 0 or k > n - 1:
            return None
        A = [[0] * n for _ in range(n)]
        degree_count = [0] * n
        edges_added = set()
        
        while sum(degree_count) < k * n:
            u = random.randint(0, n-1)
            v = random.randint(0, n-1)
            if u == v or A[u][v] != 0 or (u, v) in edges_added:
                continue
            A[u][v] = 1
            A[v][u] = 1
            degree_count[u] += 1
            degree_count[v] += 1
            edges_added.add((u, v))
        
        return A
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        rank = 0
        
        for i in range(n):
            pivot_row = -1
            for j in range(rank, m):
                if A[j][i] != 0:
                    pivot_row = j
                    break
            
            if pivot_row == -1:
                continue
            
            A[pivot_row], A[rank] = A[rank], A[pivot_row]
            rank += 1
            
            for j in range(m):
                if j != rank - 1:
                    factor = A[j][i] / A[rank-1][i]
                    for k in range(n):
                        A[j][k] -= factor * A[rank-1][k]
        
        return rank
    
    def calculate_mfr(G, k):
        n = len(G)
        eigenvalues = []
        
        # Compute the adjacency matrix
        A = G
        
        # Compute the characteristic polynomial using Gaussian elimination
        char_poly = [1]
        for i in range(n):
            char_poly = [c * x - sum(A[i][j] * char_poly[j] for j in range(i)) for x in char_poly]
        
        # The constant term of the characteristic polynomial is (-1)^n det(A)
        det_A = char_poly[-2]
        if n % 2 == 0:
            det_A = -det_A
        
        # The eigenvalues are the roots of the characteristic polynomial
        # For simplicity, we use a numerical method to find the roots
        def f(x):
            return sum([c * x**i for i, c in enumerate(char_poly[::-1])])
        
        def derivative_f(x):
            return sum([i * c * x**(i-1) for i, c in enumerate(char_poly[::-1]) if i > 0])
        
        # Newton's method to find the roots
        tol = 1e-6
        max_iter = 1000
        for _ in range(n):
            root = random.uniform(-10, 10)
            for _ in range(max_iter):
                f_val = f(root)
                df_val = derivative_f(root)
                if abs(df_val) < tol:
                    break
                root -= f_val / df_val
            
            eigenvalues.append(root)
        
        # The minimal rank of the modular form is the number of non-zero eigenvalues
        mfr_G = sum(1 for ev in eigenvalues if abs(ev) > tol)
        
        return mfr_G
    
    n_max = 40
    instances_tested = 0
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            k = random.randint(1, min(n-1, 4))
            G = generate_k_regular_graph(n, k)
            if G is None:
                continue
            
            mfr_G = calculate_mfr(G, k)
            instances_tested += 1
            n_max = max(n_max, n)
            
            ratio = Fraction(mfr_G, n).limit_denominator()
            expected_ratio = Fraction(n**(k/2), n).limit_denominator()
            if abs(ratio - expected_ratio) > 0.1 * expected_ratio:
                conjecture_holds = False
                counterexample = f"n={n}, k={k}, mfr(G)={mfr_G}, |G|^{k/2}={expected_ratio.numerator}/{expected_ratio.denominator}"
    
    return {
        "metric_name": "mfr/G",
        "metric_value": total_metric_value / instances_tested if instances_tested > 0 else 0.0,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(r["counterexample"] != "" for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if r["counterexample"] != "")
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")