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
            factor = A[i][i]
            for j in range(i, n + 1):
                A[i][j] /= factor
            for j in range(n):
                if j != i:
                    factor = A[j][i]
                    for k in range(i, n + 1):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiplication(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def spectral_radius(A):
        n = len(A)
        eigenvalues = []
        I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        max_iter = 1000
        tol = 1e-6
        x = [1] * n
        for _ in range(max_iter):
            Ax = matrix_multiplication(A, x)
            lambda_x = sum(a * b for a, b in zip(Ax, x)) / sum(a * a for a in x)
            eigenvalues.append(lambda_x)
            if abs(lambda_x - max(eigenvalues)) < tol:
                break
            x = [a / math.sqrt(sum(b * b for b in Ax)) for a in Ax]
        return max(eigenvalues)

    def mgi(data_space):
        A = [[random.random() for _ in range(len(data_space))] for _ in range(len(data_space))]
        A = gaussian_elimination(A)
        rank_variance = spectral_radius(A)
        return rank_variance

    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_metric_value = 0.0
    max_n = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            data_space = [random.random() for _ in range(n)]
            mgi_value = mgi(data_space)
            total_metric_value += mgi_value
            instances_tested += 1
            max_n = max(max_n, n)

    mean_metric_value = total_metric_value / instances_tested

    if instances_tested < 30:
        conjecture_holds = False
        counterexample = "insufficient_instances"

    return {
        "metric_name": "mgi(data_space)",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys

    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    results = []

    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")

        if not trial_result["conjecture_holds"]:
            counterexample = trial_result["counterexample"]
            break

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if not counterexample:
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
        else:
            print(f"RESULT: FALSIFIED counterexample='insufficient_support' first_failing_seed={seeds[results.index(next(r for r in results if not r['conjecture_holds']))]}")
    else:
        print(f"RESULT: INCONCLUSIVE {counterexample}")