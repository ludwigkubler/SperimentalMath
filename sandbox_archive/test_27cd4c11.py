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
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def rank_variance(M):
        m, n = len(M), len(M[0])
        A = [row[:] + [1] for row in M]
        rref = gaussian_elimination(A)
        rank = sum(1 for row in rref if any(row[j] != 0 for j in range(n)))
        return Fraction(m * n - rank, m * n)

    def projective_plane_points(n):
        points = set()
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    point = (i, j, k)
                    if len(set(point)) == 3:
                        points.add(point)
        return list(points)

    n_values = [5, 10, 15, 20, 30, 40]
    total_points = 0
    total_variance = 0
    instances_tested = 0

    for n in n_values:
        for _ in range(5):
            M = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
            variance = rank_variance(M)
            if variance == 0:
                continue
            points = projective_plane_points(n)
            total_points += len(points)
            total_variance += variance * variance
            instances_tested += 1

    if instances_tested == 0:
        return {
            "metric_name": "Points to Variance Ratio",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }

    mean_points = total_points / instances_tested
    mean_variance = total_variance / instances_tested
    C = math.sqrt(mean_points / mean_variance) if mean_variance != 0 else float('inf')

    return {
        "metric_name": "Points to Variance Ratio",
        "metric_value": C,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": C <= 3,
        "counterexample": "" if C <= 3 else f"Counterexample: C > 3, C = {C}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(res["metric_value"] for res in results if res["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results if res["metric_value"] is not None)) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results) and any(res["counterexample"] != "" for res in results):
        counterexample = next(res["counterexample"] for res in results if res["counterexample"] != "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[next(i for i, res in enumerate(results) if not res['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")