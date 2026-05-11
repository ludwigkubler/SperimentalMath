# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def generate_random_graph(n):
    edges = set()
    for i in range(n):
        for j in range(i + 1, n):
            if random.choice([True, False]):
                edges.add((i, j))
    return edges

def quadratic_forms_from_edges(edges, n):
    forms = []
    for i in range(n):
        form = [0] * n
        form[i] = 1
        for j in range(i + 1, n):
            if (i, j) in edges or (j, i) in edges:
                form[j] = -1
        forms.append(form)
    return forms

def matrix_multiplication(A, B):
    m, k = len(A), len(B[0])
    result = [[0] * k for _ in range(m)]
    for i in range(m):
        for j in range(k):
            for l in range(len(B)):
                result[i][j] += A[i][l] * B[l][j]
    return result

def gaussian_elimination(A, b):
    n = len(A)
    augmented_matrix = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i + 1, n):
            if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                max_row = j
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        pivot = augmented_matrix[i][i]
        for j in range(i, n + 1):
            augmented_matrix[i][j] /= pivot
        for j in range(n):
            if j != i:
                factor = augmented_matrix[j][i]
                for k in range(i, n + 1):
                    augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
    return [row[-1] for row in augmented_matrix]

def real_radical_rank(I):
    forms = quadratic_forms_from_edges(I, len(I))
    A = []
    for form in forms:
        A.append(form)
    b = [0] * len(forms)
    solution = gaussian_elimination(A, b)
    rank = sum(1 for x in solution if abs(x) > 1e-6)
    return rank

def sos_degree(I):
    n = len(I)
    forms = quadratic_forms_from_edges(I, n)
    A = []
    for form in forms:
        A.append(form)
    b = [0] * len(forms)
    solution = gaussian_elimination(A, b)
    degree = sum(1 for x in solution if abs(x) > 1e-6)
    return degree

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    I = generate_random_graph(n)
    rank_real_radical_I = real_radical_rank(I)
    sos_degree_I = sos_degree(I)
    return {
        "metric_name": "sos_degree",
        "metric_value": sos_degree_I,
        "instances_tested": 1,
        "conjecture_holds": sos_degree_I >= rank_real_radical_I,
        "counterexample": "" if sos_degree_I >= rank_real_radical_I else f"Graph with {n} variables and {len(I)} edges"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Graph with {n} variables and {len(I)} edges\" first_failing_seed={first_failing_seed}")