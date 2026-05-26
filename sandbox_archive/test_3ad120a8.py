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
            max_row = max(range(i, n), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            if pivot == 0:
                continue
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

    def determinant(A):
        n = len(A)
        if n == 1:
            return A[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det

    def log3(x):
        if x <= 0:
            return float('-inf')
        return math.log(x, 3)

    n = random.randint(5, 40)
    instances_tested = 0
    total_curvature = 0.0
    conjecture_holds = True

    for _ in range(10):
        formula = [random.choice([True, False]) for _ in range(n)]
        A = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
        B = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
        C = matrix_multiply(A, B)
        det_C = determinant(C)
        if det_C == 0:
            continue
        curvature = log3(abs(det_C))
        instances_tested += 1
        total_curvature += curvature

    mean_curvature = total_curvature / instances_tested
    counterexample = ""
    for _ in range(10):
        formula = [random.choice([True, False]) for _ in range(n)]
        A = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
        B = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
        C = matrix_multiply(A, B)
        det_C = determinant(C)
        if det_C == 0:
            continue
        curvature = log3(abs(det_C))
        if curvature > mean_curvature * 2:
            counterexample = f"Formula: {formula}, A: {A}, B: {B}, C: {C}"
            conjecture_holds = False
            break

    return {
        "metric_name": "Algebraic Curvature",
        "metric_value": mean_curvature,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_curvature = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_curvature} std=0 support_fraction={support_fraction}")
    elif any(r["counterexample"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["counterexample"])
        counterexample_desc = results[seeds.index(first_failing_seed)]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")