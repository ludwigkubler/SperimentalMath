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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_rank(matrix):
    if not matrix or not matrix[0]:
        return 0
    rows, cols = len(matrix), len(matrix[0])
    rank = 0
    for col in range(cols):
        pivot_row = -1
        for row in range(rank, rows):
            if matrix[row][col] != 0:
                pivot_row = row
                break
        if pivot_row == -1:
            continue
        matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
        for r in range(rows):
            if r != rank and matrix[r][col] != 0:
                factor = Fraction(matrix[r][col], matrix[rank][col])
                for c in range(cols):
                    matrix[r][c] -= factor * matrix[rank][c]
        rank += 1
    return rank

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for col in range(cols):
        pivot_row = -1
        for row in range(col, rows):
            if matrix[row][col] != 0:
                pivot_row = row
                break
        if pivot_row == -1:
            continue
        matrix[pivot_row], matrix[col] = matrix[col], matrix[pivot_row]
        for r in range(rows):
            if r != col and matrix[r][col] != 0:
                factor = Fraction(matrix[r][col], matrix[col][col])
                for c in range(cols):
                    matrix[r][c] -= factor * matrix[col][c]
    return matrix

def generate_k_clique_instance(n, k):
    vertices = list(range(n))
    edges = []
    for i in range(k):
        for j in range(i + 1, k):
            edges.append((vertices[i], vertices[j]))
    for _ in range(random.randint(0, n * (n - 1) // 2 - len(edges))):
        u, v = random.sample(vertices, 2)
        if (u, v) not in edges and (v, u) not in edges:
            edges.append((u, v))
    return vertices, edges

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        instances_tested = 0
        total_rank = 0
        for _ in range(5):  # Test each n with 5 different k values
            k = random.randint(n // 2, n)
            vertices, edges = generate_k_clique_instance(n, k)
            # Construct the Boolean differential form (simplified example)
            form = [[1 if (i, j) in edges else 0 for j in range(n)] for i in range(n)]
            rank = matrix_rank(gaussian_elimination(form))
            total_rank += rank
            instances_tested += 1
        avg_rank = Fraction(total_rank, instances_tested)
        expected_rank = n ** Fraction(1, 4)
        if abs(avg_rank - expected_rank) > 3 * (expected_rank / math.sqrt(instances_tested)):
            return {
                "metric_name": "rank",
                "metric_value": float(avg_rank),
                "instances_tested": instances_tested,
                "conjecture_holds": False,
                "counterexample": f"n={n}, avg_rank={avg_rank}, expected_rank={expected_rank}"
            }
    return {
        "metric_name": "rank",
        "metric_value": float(avg_rank),
        "instances_tested": instances_tested * len(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    avg_rank = sum(r['metric_value'] for r in results) / len(results)
    std_dev = math.sqrt(sum((r['metric_value'] - avg_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_rank} std={std_dev} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results):
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"rank_discrepancy\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")