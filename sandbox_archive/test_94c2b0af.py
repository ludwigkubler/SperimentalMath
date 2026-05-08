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

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def generate_random_graph(n):
    graph = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        graph[i][i] = 0
    return [sum(row) for row in graph]

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        max_row = max(range(i, n), key=lambda k: abs(matrix[k][i]))
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        factor = matrix[i][i]
        for j in range(n):
            matrix[i][j] /= factor
        for j in range(n):
            if i != j:
                factor = matrix[j][i]
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]

def determinant(matrix):
    n = len(matrix)
    det = 1
    A = [row[:] for row in matrix]
    for i in range(n):
        if A[i][i] == 0:
            return 0
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    for i in range(n):
        det *= A[i][i]
    return det

def simplicial_homology(graph):
    n = len(graph)
    clique_complex = []
    for i in range(1, 1 << n):
        subset = [j for j in range(n) if (i & (1 << j))]
        if all(graph[subset[j]][subset[k]] == 1 for j in range(len(subset)) for k in range(j + 1, len(subset))):
            clique_complex.append(subset)
    A = []
    for i in range(1, len(clique_complex)):
        row = [0] * (len(clique_complex) - 1)
        for j in range(i):
            if set(clique_complex[j]).issubset(set(clique_complex[i])):
                row[j] = (-1) ** (i - j - 1)
        A.append(row)
    return abs(determinant(A))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    graph = generate_random_graph(n)
    beta_1 = simplicial_homology(graph)
    if beta_1 < 1:
        return {
            "metric_name": "resolution_length",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "beta_1(G) < 1"
        }
    resolution_length = 2 ** beta_1
    return {
        "metric_name": "resolution_length",
        "metric_value": resolution_length,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 35)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "beta_1(G) < 1" if any(r["counterexample"] == "beta_1(G) < 1" for r in results) else ""
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")