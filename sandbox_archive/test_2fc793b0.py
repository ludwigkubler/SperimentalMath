# auto-injected by SEC sandbox
import json
import os
import time
import re
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import itertools
from collections import defaultdict

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
    for i in range(len(edges)):
        for j in range(i + 1, len(edges)):
            a, b = edges[i]
            c, d = edges[j]
            if len({a, b, c, d}) == 3:
                triangles.append((edges[i], edges[j]))
    matrix = []
    for triangle in triangles:
        row = [0] * n
        for edge in triangle:
            row[edges.index(edge)] = 1
        matrix.append(row)
    return matrix

def generate_random_monotone_function(n, s, w):
    terms = set()
    while len(terms) < s:
        term = tuple(sorted(random.sample(range(n), w)))
        terms.add(term)
    minterms = set()
    for term in terms:
        minterms.update(itertools.combinations(term, len(term)))
    matrix = []
    for minterm in minterms:
        row = [0] * n
        for var in minterm:
            row[var] = 1
        matrix.append(row)
    return matrix

def generate_threshold_matrix(n, k):
    matrix = []
    for bits in itertools.product([0, 1], repeat=n):
        if sum(bits) == k:
            matrix.append(list(bits))
    return matrix

def run_trial(seed):
    random.seed(seed)
    metric_name = "mu_2_over_L_DNF_log2_L_DNF_plus_2"
    metric_value = 0.0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    # Test CLIQUE instances
    for v in range(4, 9):
        n = v * (v - 1) // 2
        matrix = generate_clique_matrix(v)
        rank = gaussian_elimination(matrix)
        mu_2 = len(matrix) - rank
        expected_mu_2 = (v - 1) * (v - 2) * (v - 3) // 6
        if mu_2 != expected_mu_2:
            conjecture_holds = False
            counterexample = f"CLIQUE_{v,3} has mu_2={mu_2} != {expected_mu_2}"
            break

    if conjecture_holds:
        # Test random monotone functions
        for n in [8, 12, 16, 20]:
            for s in [3, 5, 8]:
                for w in [3]:
                    for _ in range(30):
                        matrix = generate_random_monotone_function(n, s, w)
                        rank = gaussian_elimination(matrix)
                        mu_2 = len(matrix) - rank
                        L_DNF = s * w
                        bound = L_DNF * math.log2(L_DNF + 2)
                        if mu_2 > bound:
                            conjecture_holds = False
                            counterexample = f"Random monotone function with n={n}, s={s}, w={w} has mu_2={mu_2} > {bound}"
                            break
                        instances_tested += 1
                    if not conjecture_holds:
                        break
                if not conjecture_holds:
                    break
            if not conjecture_holds:
                break

    if conjecture_holds:
        # Test threshold instances
        for n in [6, 8, 10, 12, 14, 16]:
            for k in [2, 3]:
                matrix = generate_threshold_matrix(n, k)
                rank = gaussian_elimination(matrix)
                mu_2 = len(matrix) - rank
                L_DNF = k * math.comb(n, k)
                bound = L_DNF * math.log2(L_DNF + 2)
                if mu_2 > bound:
                    conjecture_holds = False
                    counterexample = f"Threshold function with n={n}, k={k} has mu_2={mu_2} > {bound}"
                    break
                instances_tested += 1
            if not conjecture_holds:
                break

    if conjecture_holds:
        # Test k=4 CLIQUE instances
        for v in [5, 6, 7]:
            n = v * (v - 1) // 2
            matrix = generate_clique_matrix(v)
            rank = gaussian_elimination(matrix)
            mu_2 = len(matrix) - rank
            metric_value += mu_2 / len(matrix)

    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
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
    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")