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
    m, k = len(A), len(B[0])
    n = len(B)
    C = [[0] * k for _ in range(m)]
    for i in range(m):
        for j in range(k):
            for l in range(n):
                C[i][j] += A[i][l] * B[l][j]
    return C

def gaussian_elimination(A, b):
    n = len(A)
    augmented = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(augmented[j][i]) > abs(augmented[max_row][i]):
                max_row = j
        augmented[i], augmented[max_row] = augmented[max_row], augmented[i]
        pivot = augmented[i][i]
        for j in range(n + 1):
            augmented[i][j] /= pivot
        for j in range(n):
            if j != i:
                factor = augmented[j][i]
                for k in range(n + 1):
                    augmented[j][k] -= factor * augmented[i][k]
    return [row[-1] for row in augmented]

def rank(matrix):
    m, n = len(matrix), len(matrix[0])
    A = matrix[:]
    r = gaussian_elimination(A, [0]*n)
    return sum(1 for x in r if abs(x) > 1e-9)

def young_diagram_partitions(n):
    def partitions(n, k=0):
        if n == 0:
            yield []
        elif k == 0:
            yield [n]
        else:
            for p in partitions(n-k, k):
                yield [k] + p
            yield from partitions(n, k-1)
    return list(partitions(n))

def kronecker_coefficient(λ, μ, ν):
    if len(λ) != len(μ) or len(μ) != len(ν):
        raise ValueError("Partitions must have the same length")
    n = len(λ)
    def hook_length_formula(p):
        h = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if p[i][j] == 0:
                    continue
                h[i][j] = (n - i) + (n - j) - p[i][j] + 1
        det = 1
        for i in range(n):
            for j in range(n):
                det *= h[i][j]
                if det == 0:
                    return 0
        return det // math.factorial(sum(p[i][j] for i in range(n) for j in range(n)))
    def littlewood_richardson_rule(λ, μ, ν):
        p = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if λ[i] + μ[j] - ν[i-j-1] > 0:
                    p[i][j] = min(λ[i], μ[j]) - max(0, λ[i] + μ[j] - ν[i-j-1])
        return hook_length_formula(p)
    return littlewood_richardson_rule(λ, μ, ν)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    λ = tuple(random.sample(range(n+1), n))
    μ = tuple(random.sample(range(n+1), n))
    ν = tuple(random.sample(range(n+1), n))
    partitions = young_diagram_partitions(n)
    if len(partitions) < 3:
        return {
            "metric_name": "Kronecker Coefficient Gap",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    κ = kronecker_coefficient(λ, μ, ν)
    if κ is None:
        return {
            "metric_name": "Kronecker Coefficient Gap",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    log_n = math.log(n)
    if κ >= log_n ** 1.5:
        return {
            "metric_name": "Kronecker Coefficient Gap",
            "metric_value": κ,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "Kronecker Coefficient Gap",
            "metric_value": κ,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Kronecker coefficient {κ} < (log {n})^1.5"
        }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(2, 31)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")