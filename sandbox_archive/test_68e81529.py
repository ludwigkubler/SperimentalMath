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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B[0]), len(B)
        C = [[0]*n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def hodge_dimension(poly, p):
        n = len(poly)
        A = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(i+1):
                A[i][j] = poly[i] - poly[j]
        A = gaussian_elimination(A)
        rank = sum(1 for row in A if any(row))
        return n - rank
    
    def resolution_width(phi, p):
        # Placeholder for actual resolution width computation
        # This is a dummy implementation and should be replaced with the actual algorithm
        return len(phi)  # Simplified as length of phi for demonstration purposes
    
    def generate_k_cnf(n, k):
        clauses = []
        variables = list(range(1, n+1))
        for _ in range(k):
            clause = random.sample(variables, random.randint(1, n))
            if random.choice([True, False]):
                clause = [-v for v in clause]
            clauses.append(clause)
        return clauses
    
    def clause_indicator_polynomial(phi, p):
        n = len(phi[0])
        poly = [1] * (n + 1)
        for clause in phi:
            term = 1
            for var in clause:
                if var > 0:
                    term *= (1 - x[var-1])
                else:
                    term *= (1 + x[-var-1])
            poly = [sum(a*b for a, b in zip(p1, p2)) % p for p1, p2 in zip(poly, term)]
        return poly
    
    def generate_random_instance(n, k, p):
        phi = generate_k_cnf(n, k)
        x = [random.randint(0, p-1) for _ in range(n)]
        poly = clause_indicator_polynomial(phi, p)
        h = hodge_dimension(poly, p)
        w = resolution_width(phi, p)
        return {"h": h, "w": w}
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        instances_tested = 0
        total_h = 0
        total_w = 0
        max_n = n
        for _ in range(30):
            instance = generate_random_instance(n, random.randint(1, n), random.choice([2, 3, 5]))
            h = instance["h"]
            w = instance["w"]
            instances_tested += 1
            total_h += h
            total_w += w
        mean_h = Fraction(total_h, instances_tested)
        mean_w = Fraction(total_w, instances_tested)
        ratio = mean_h / mean_w if mean_w != 0 else float('inf')
        results.append({"n": n, "mean_h": mean_h, "mean_w": mean_w, "ratio": ratio})
    
    h_values = [result["mean_h"] for result in results]
    w_values = [result["mean_w"] for result in results]
    mean_ratio = sum(result["ratio"] for result in results) / len(results)
    std_ratio = math.sqrt(sum((result["ratio"] - mean_ratio)**2 for result in results) / len(results))
    
    conjecture_holds = 0.5 <= mean_ratio <= 2 and std_ratio <= 0.3
    counterexample = "" if conjecture_holds else f"mean_ratio={mean_ratio}, std_ratio={std_ratio}"
    
    return {
        "metric_name": "Ratio of Hodge Dimension to Resolution Width",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested * len(n_values),
        "n_max": max_n,
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
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if 0.5 <= r["metric_value"] <= 2 and abs(r["metric_value"] - mean_ratio) <= 0.3) / len(results)
    
    if all(0.5 <= r["metric_value"] <= 2 and abs(r["metric_value"] - mean_ratio) <= 0.3 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any(not (0.5 <= r["metric_value"] <= 2 and abs(r["metric_value"] - mean_ratio) <= 0.3) for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not (0.5 <= result["metric_value"] <= 2 and abs(result["metric_value"] - mean_ratio) <= 0.3))
        print(f"RESULT: FALSIFIED counterexample=\"mean_ratio={result['metric_value']}, std_ratio={std_ratio}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")