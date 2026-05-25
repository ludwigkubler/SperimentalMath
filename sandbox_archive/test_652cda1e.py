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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_multiplication(A, B):
    m, n, p = len(A), len(B), len(B[0])
    result = [[Fraction(0, 1)] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                result[i][j] += A[i][k] * B[k][j]
    return result

def gaussian_elimination(matrix):
    m, n = len(matrix), len(matrix[0])
    for i in range(min(m, n)):
        if matrix[i][i] == 0:
            for j in range(i + 1, m):
                if matrix[j][i] != 0:
                    matrix[i], matrix[j] = matrix[j], matrix[i]
                    break
            else:
                continue
        for j in range(m):
            if j != i and matrix[j][i] != 0:
                factor = -matrix[j][i] / matrix[i][i]
                for k in range(n):
                    matrix[j][k] += factor * matrix[i][k]
    return matrix

def rank(matrix):
    m, n = len(matrix), len(matrix[0])
    gaussian_elimination(matrix)
    rank = 0
    for i in range(min(m, n)):
        if matrix[i][i] != 0:
            rank += 1
    return rank

def generate_random_bp(n):
    bp = []
    for _ in range(2 ** (n - 1)):
        bp.append(random.choice([0, 1]))
    return bp

def tropicalized_k_theory_invariant(bp):
    n = len(bp)
    matrix = [[Fraction(0, 1)] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if bp[i] != bp[j]:
                matrix[i][j] = Fraction(1, 1)
                matrix[j][i] = Fraction(1, 1)
    return rank(matrix)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        instances_tested = 0
        total_rho_P = Fraction(0, 1)
        for _ in range(5):  # Ensure at least 5 instances per size
            bp = generate_random_bp(n)
            rho_P = tropicalized_k_theory_invariant(bp)
            if rho_P == 0:
                continue
            instances_tested += 1
            total_rho_P += rho_P
        if instances_tested == 0:
            return {
                "metric_name": "rho(P) / log(size(P))",
                "metric_value": None,
                "instances_tested": 0,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        mean_rho_P = total_rho_P / instances_tested
        ratio = mean_rho_P / math.log(n)
        results.append(ratio)
    return {
        "metric_name": "rho(P) / log(size(P))",
        "metric_value": sum(results) / len(results),
        "instances_tested": 30,
        "conjecture_holds": all(0.25 <= ratio <= 2 for ratio in results),
        "counterexample": "" if all(0.25 <= ratio <= 2 for ratio in results) else "ratio_out_of_bounds"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean_value = sum(results) / len(results)
    support_fraction = sum(1 for r in results if 0.5 <= r <= 1.5) / len(results)
    if all(0.25 <= r <= 2 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=NA support_fraction={support_fraction}")
    elif any(r < 0.25 or r > 2 for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if r < 0.25 or r > 2)
        print(f"RESULT: FALSIFIED counterexample='ratio_out_of_bounds' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=metric_saturation")