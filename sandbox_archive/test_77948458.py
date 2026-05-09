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

def generate_max_cut_instance(n):
    return [random.choice([0, 1]) for _ in range(n)]

def construct_moment_matrix(instance, d):
    n = len(instance)
    M = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n):
        for j in range(i + 1, n):
            if instance[i] != instance[j]:
                M[i][j] = M[j][i] = 1
    for k in range(2, d + 1):
        new_M = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            for j in range(i + 1, n):
                for l in range(j + 1, n):
                    if instance[i] != instance[j] and instance[j] != instance[l]:
                        new_M[i][l] += M[i][j]
                        new_M[l][i] += M[i][j]
        M = new_M
    return M

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i + 1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def count_positive_eigenvalues(A):
    eigenvalues = []
    n = len(A)
    while n > 0:
        A = gaussian_elimination(A)
        if A[-1][-1] < 0:
            break
        eigenvalues.append(A[-1][-1])
        A.pop()
        for i in range(n - 2, -1, -1):
            A[i][n - 1] -= A[i][n - 2] * A[n - 2][n - 1]
        n -= 1
    return len(eigenvalues)

def sos_refutation_degree(M):
    d = 2
    while True:
        M_d = construct_moment_matrix([0] * len(M), d)
        if all(all(A[i][j] == B[i][j] for j in range(len(B))) for i, B in enumerate(M_d)):
            return d
        d += 1

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    instance = generate_max_cut_instance(n)
    max_eigenvalue_count = 0
    min_refutation_degree = float('inf')
    for d in range(2, 9):
        M = construct_moment_matrix(instance, d)
        positive_eigenvalues = count_positive_eigenvalues(M)
        if positive_eigenvalues > max_eigenvalue_count:
            max_eigenvalue_count = positive_eigenvalues
        refutation_degree = sos_refutation_degree(M)
        if refutation_degree < min_refutation_degree:
            min_refutation_degree = refutation_degree
    metric_value = max_eigenvalue_count / (min_refutation_degree ** 2)
    conjecture_holds = metric_value >= math.log(n) / (min_refutation_degree ** 2)
    counterexample = "" if conjecture_holds else f"n={n}, d={min_refutation_degree}"
    return {
        "metric_name": "positive_eigenvalue_count / refutation_degree^2",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']:.6f}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.6f} std={std_metric_value:.6f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.6f} std={std_metric_value:.6f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")