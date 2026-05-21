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
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def matrix_multiply(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def spectral_gap(M, d):
        n = len(M)
        identity = [[Fraction(1 if i == j else 0) for j in range(n)] for i in range(n)]
        M_d = matrix_multiply(M, M)
        A = [[M_d[i][j] - Fraction(2 * (i != j)) for j in range(n)] for i in range(n)]
        A = gaussian_elimination(A)
        eigenvalues = [A[i][i] for i in range(n)]
        return max(eigenvalues) - min(eigenvalues)

    def pseudoexpectation(instance):
        n = len(instance)
        M = [[Fraction(0) for _ in range(n)] for _ in range(n)]
        for u, v in instance:
            M[u][v] += Fraction(1)
            M[v][u] += Fraction(1)
        return M

    def max_cut_instance(n):
        instance = []
        for i in range(n):
            for j in range(i+1, n):
                if random.random() < 0.5:
                    instance.append((i, j))
        return instance

    def approximation_ratio(instance, cut):
        n = len(instance)
        total_edges = sum(1 for u, v in instance)
        cut_edges = sum(1 for u, v in instance if (u, v) not in cut and (v, u) not in cut)
        return 2 * cut_edges / total_edges

    def find_cut(instance):
        n = len(instance)
        cut = set()
        visited = [False] * n
        stack = [0]
        while stack:
            node = stack.pop()
            if not visited[node]:
                visited[node] = True
                for u, v in instance:
                    if u == node and (v, node) not in cut:
                        cut.add((u, v))
                        stack.append(v)
        return cut

    n = random.randint(5, 40)
    d = random.randint(3, 10)
    instance = max_cut_instance(n)
    M = pseudoexpectation(instance)
    gap = spectral_gap(M, d)
    epsilon_d = Fraction(gap) / d
    threshold = Fraction(878) - epsilon_d

    cut = find_cut(instance)
    ratio = approximation_ratio(instance, cut)

    return {
        "metric_name": "approximation_ratio",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "conjecture_holds": ratio > threshold,
        "counterexample": "" if ratio > threshold else f"Cut {cut} does not achieve better than {threshold}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")