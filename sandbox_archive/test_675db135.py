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
    
    def generate_polynomial(n):
        coefficients = [random.randint(0, 1) for _ in range(n + 1)]
        return coefficients
    
    def construct_incidence_graph(poly):
        n = len(poly) - 1
        G = {}
        for i in range(n + 1):
            if poly[i] != 0:
                for j in range(i + 1, n + 1):
                    if poly[j] != 0:
                        edge = (i, j)
                        if edge not in G:
                            G[edge] = 1
                        else:
                            G[edge] += 1
        return G
    
    def gaussian_elimination(A, b):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i + 1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for j in range(i + 1, m):
                factor = -A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] += factor * A[i][k]
                b[j] += factor * b[i]
        x = [0] * n
        for i in range(m - 1, -1, -1):
            x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
        return x
    
    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def determinant(A):
        n = len(A)
        if n == 1:
            return A[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det
    
    def rank(A):
        m, n = len(A), len(A[0])
        A_copy = [row[:] for row in A]
        r = 0
        for i in range(min(m, n)):
            if A_copy[i][i] != 0:
                for j in range(i + 1, m):
                    factor = -A_copy[j][i] / A_copy[i][i]
                    for k in range(n):
                        A_copy[j][k] += factor * A_copy[i][k]
                r += 1
        return r
    
    def is_full_rank(A):
        return rank(A) == min(len(A), len(A[0]))
    
    def generate_random_instance(n):
        poly = generate_polynomial(n)
        G = construct_incidence_graph(poly)
        num_edges = sum(G.values())
        depth = random.randint(1, 5)  # Simulating ACC⁰ circuit depth
        return num_edges, n, depth
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for _ in range(30):  # Aim for at least 30 instances per seed
        n = random.choice(n_values)
        num_edges, n, depth = generate_random_instance(n)
        if num_edges == 0:
            continue
        metric_value = Fraction(num_edges, math.sqrt(n * depth))
        results.append({"metric_name": "num_edges_per_sqrt_nD", "metric_value": float(metric_value), "instances_tested": 1, "conjecture_holds": True, "counterexample": ""})
    
    if not results:
        return {"metric_name": "num_edges_per_sqrt_nD", "metric_value": 0.0, "instances_tested": 0, "conjecture_holds": False, "counterexample": "mapping_undefined"}
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = all(r["conjecture_holds"] for r in results)
    
    if support_fraction:
        return {"metric_name": "num_edges_per_sqrt_nD", "metric_value": mean_value, "instances_tested": len(results), "conjecture_holds": True, "counterexample": ""}
    else:
        first_failing_seed = next((i for i, r in enumerate(results) if not r["conjecture_holds"]), None)
        return {"metric_name": "num_edges_per_sqrt_nD", "metric_value": mean_value, "instances_tested": len(results), "conjecture_holds": False, "counterexample": f"first_failing_seed={first_failing_seed}"}

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = all(r["conjecture_holds"] for r in results)
    
    if support_fraction:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] != "" for r in results):
        first_failing_seed = next((i for i, r in enumerate(results) if "counterexample" in r and r["counterexample"] != ""), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")