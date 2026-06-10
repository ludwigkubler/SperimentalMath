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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_multiply(A, B):
    m, k = len(A), len(B)
    n = len(B[0])
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for l in range(k):
                C[i][j] += A[i][l] * B[l][j]
    return C

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    Augmented = [A[i] + [b[i]] for i in range(m)]
    for j in range(n):
        max_row = j
        for i in range(j+1, m):
            if abs(Augmented[i][j]) > abs(Augmented[max_row][j]):
                max_row = i
        Augmented[j], Augmented[max_row] = Augmented[max_row], Augmented[j]
        pivot = Augmented[j][j]
        for i in range(j, n+1):
            Augmented[j][i] /= pivot
        for i in range(m):
            if i != j:
                factor = Augmented[i][j]
                for k in range(j, n+1):
                    Augmented[i][k] -= factor * Augmented[j][k]
    return [row[-1] for row in Augmented]

def determinant(A):
    m, n = len(A), len(A[0])
    if m != n:
        raise ValueError("Matrix must be square")
    if n == 1:
        return A[0][0]
    det = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det += (-1) ** j * A[0][j] * determinant(submatrix)
    return det

def rank(A):
    m, n = len(A), len(A[0])
    RREF = gaussian_elimination(A, [0] * m)
    rank = 0
    for row in RREF:
        if any(row):
            rank += 1
    return rank

def geometric_invariant_rank(phi_G):
    det_phi_G = determinant(phi_G)
    if det_phi_G == 0:
        return 0
    return rank(phi_G)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n, m = random.randint(5, 40), random.randint(5, 40)
    phi_G = [[random.randint(-10, 10) for _ in range(m)] for _ in range(n)]
    rank_variance = sum(sum(row[i] - row[j] for i in range(i+1, m)) ** 2 for row in phi_G for j in range(j+1, n))
    gir_phi_G = geometric_invariant_rank(phi_G)
    if gir_phi_G == 0:
        return {
            "metric_name": "gir/phi_G",
            "metric_value": gir_phi_G,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    ratio = gir_phi_G / rank_variance
    return {
        "metric_name": "gir/phi_G",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(ratio - 1) <= 0.1 or ratio > 1.1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] if sys.argv[1:] else [random.randint(2, 1000003) for _ in range(30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)

    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] and res["counterexample"] == "" for res in results):
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"] and res["counterexample"] == "")
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")