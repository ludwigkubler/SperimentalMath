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
            for j in range(n):
                A[i][j] /= factor
            for j in range(n):
                if i != j:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiply(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
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
        return sum(1 for row in gaussian_elimination(A) if any(row))

    def median(lst):
        n = len(lst)
        sorted_lst = sorted(lst)
        mid = n // 2
        if n % 2 == 0:
            return (sorted_lst[mid - 1] + sorted_lst[mid]) / 2.0
        else:
            return sorted_lst[mid]

    def local_coherence_index(A):
        det_A = determinant(A)
        rank_A = rank(A)
        if det_A == 0 or rank_A == 0:
            return 0
        return abs(det_A) ** (1 / rank_A)

    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_I = 0.0
    total_V_R = 0.0
    n_max = 0

    for n in n_values:
        for _ in range(5):
            R = random.randint(1, n)
            V = sum(random.random() * (n - i) for i in range(n))
            A = [[random.random() for _ in range(n)] for _ in range(n)]
            I = local_coherence_index(A)
            total_I += I
            total_V_R += V / R
            instances_tested += 1
            n_max = max(n_max, n)

    if instances_tested < 30:
        return {
            "metric_name": "I/V_R",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }

    mean_I = total_I / instances_tested
    mean_V_R = total_V_R / instances_tested

    def linear_regression(x, y):
        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(xi * yi for xi, yi in zip(x, y))
        sum_xx = sum(xi ** 2 for xi in x)
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x ** 2)
        intercept = (sum_y - slope * sum_x) / n
        return slope, intercept

    slope, _ = linear_regression([mean_I], [mean_V_R])
    if abs(slope - 1) < 0.05:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "I/V_R ratio does not match V/R"

    return {
        "metric_name": "I/V_R",
        "metric_value": slope,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")

    mean_I = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_I = math.sqrt(sum((result["metric_value"] - mean_I) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_I} std={std_I} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_I} std={std_I} support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={seed}")
                break