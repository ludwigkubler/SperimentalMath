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
    
    def generate_max_cut_instance(n):
        vertices = list(range(n))
        edges = [(i, j) for i in range(n) for j in range(i + 1, n)]
        cut_edges = random.sample(edges, k=int(n * (n - 1) / 4))
        return vertices, cut_edges
    
    def construct_sos_moment_matrix(vertices, cut_edges, d):
        n = len(vertices)
        M_d = [[0] * n for _ in range(n)]
        for i in range(n):
            M_d[i][i] = Fraction(1, 2)
        for u, v in edges:
            if (u, v) not in cut_edges and (v, u) not in cut_edges:
                M_d[u][v] = M_d[v][u] = Fraction(1, 4)
        return M_d
    
    def compute_real_rank(matrix):
        n = len(matrix)
        for i in range(n):
            if matrix[i][i] == 0:
                continue
            for j in range(i + 1, n):
                factor = -matrix[j][i] / matrix[i][i]
                for k in range(n):
                    matrix[j][k] += factor * matrix[i][k]
        rank = sum(1 for row in matrix if any(row))
        return rank
    
    def eigenvalue_decomposition(matrix):
        n = len(matrix)
        eigenvalues = []
        A = [row[:] for row in matrix]
        for _ in range(n):
            max_index = 0
            for i in range(1, n):
                if abs(A[i][i]) > abs(A[max_index][max_index]):
                    max_index = i
            A[0], A[max_index] = A[max_index], A[0]
            pivot = A[0][0]
            for j in range(n):
                A[0][j] /= pivot
            for i in range(1, n):
                factor = -A[i][0]
                for j in range(n):
                    A[i][j] += factor * A[0][j]
            eigenvalues.append(A[0][0])
        return eigenvalues
    
    def real_rank(matrix):
        eigenvals = eigenvalue_decomposition(matrix)
        return sum(1 for val in eigenvals if abs(val) > 1e-10)
    
    n = random.randint(5, 40)
    d = random.randint(2, 4)
    vertices, cut_edges = generate_max_cut_instance(n)
    M_d = construct_sos_moment_matrix(vertices, cut_edges, d)
    rank = real_rank(M_d)
    
    metric_name = "real_rank"
    metric_value = rank
    instances_tested = 1
    conjecture_holds = rank >= 0.8 * d ** 2
    counterexample = "" if conjecture_holds else f"rank={rank}, expected ≥{0.8 * d ** 2}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='{result['counterexample']}' first_failing_seed={first_failing_seed}")