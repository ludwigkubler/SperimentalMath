# auto-injected by SEC sandbox
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import itertools
from fractions import Fraction

def gaussian_elimination(matrix):
    rows = len(matrix)
    if rows == 0:
        return 0
    cols = len(matrix[0])
    rank = 0
    for col in range(cols):
        pivot = -1
        for row in range(rank, rows):
            if matrix[row][col] == 1:
                pivot = row
                break
        if pivot == -1:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        for row in range(rows):
            if row != rank and matrix[row][col] == 1:
                for c in range(col, cols):
                    matrix[row][c] = (matrix[row][c] + matrix[rank][c]) % 2
        rank += 1
    return rank

def generate_clique_matrix(v):
    n = v * (v - 1) // 2
    edges = list(itertools.combinations(range(v), 2))
    triangles = []
    for i, j in edges:
        for k in range(v):
            if k != i and k != j and (i, k) in edges and (j, k) in edges:
                triangles.append((i, j, k))
    matrix = []
    for i, j, k in triangles:
        row = [0] * n
        edge_indices = {edge: idx for idx, edge in enumerate(edges)}
        row[edge_indices[(i, j)]] = 1
        row[edge_indices[(i, k)]] = 1
        row[edge_indices[(j, k)]] = 1
        matrix.append(row)
    return matrix

def generate_random_monotone_function(n, s, w):
    terms = set()
    while len(terms) < s:
        term = frozenset(random.sample(range(n), w))
        terms.add(term)
    minterms = set()
    for term in terms:
        minterms.update(itertools.product(*[[0, 1] if i in term else [0] for i in range(n)]))
    minterms = [list(m) for m in minterms]
    return minterms

def compute_mu2(matrix):
    rank = gaussian_elimination(matrix)
    return len(matrix) - rank

def run_trial(seed):
    random.seed(seed)
    metric_value = 0.0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    # Test CLIQUE instances
    for v in range(4, 9):
        n = v * (v - 1) // 2
        matrix = generate_clique_matrix(v)
        mu2 = compute_mu2(matrix)
        expected_mu2 = (v - 1) * (v - 2) * (v - 3) // 6
        if mu2 != expected_mu2:
            conjecture_holds = False
            counterexample = f"CLIQUE_{v,3} has mu2={mu2} but expected {expected_mu2}"
            break
        metric_value += mu2
        instances_tested += 1

    if conjecture_holds:
        # Test random monotone functions
        for n in [8, 12, 16, 20]:
            for s in [3, 5, 8]:
                for w in [3]:
                    for _ in range(30):
                        minterms = generate_random_monotone_function(n, s, w)
                        mu2 = compute_mu2(minterms)
                        L_DNF = s * w
                        bound = L_DNF * math.log2(L_DNF + 2)
                        if mu2 > bound:
                            conjecture_holds = False
                            counterexample = f"Random monotone function with n={n}, s={s}, w={w} has mu2={mu2} > bound={bound}"
                            break
                        metric_value += mu2
                        instances_tested += 1
                    if not conjecture_holds:
                        break
                if not conjecture_holds:
                    break
            if not conjecture_holds:
                break

    return {
        "metric_name": "mu2",
        "metric_value": metric_value / instances_tested if instances_tested > 0 else 0.0,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    metric_values = [r["metric_value"] for r in results]
    mean_metric = sum(metric_values) / len(metric_values) if metric_values else 0.0
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values)) if metric_values else 0.0
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results) if results else 0.0

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        first_counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{first_counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")