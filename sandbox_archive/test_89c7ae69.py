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

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def generate_primes(n):
    primes = []
    num = 2
    while len(primes) < n:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i + max(range(i, m), key=lambda x: abs(A[x][i]))
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i + 1, m):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(m - 1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
    return x

def matrix_multiply(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def generate_projective_plane(q):
    if q < 2 or not is_prime(q) and not (q & (q - 1)) == 0:
        raise ValueError("q must be a prime power")
    points = list(range(q**2 + q + 1))
    lines = []
    for i in range(q):
        for j in range(q):
            line = [i * q + j, i * q + (j + 1) % q, (i + 1) * q + j]
            lines.append(line)
    return points, lines

def incidence_matrix(points, lines):
    m, n = len(lines), len(points)
    M = [[0] * n for _ in range(m)]
    for i, line in enumerate(lines):
        for point in line:
            M[i][point] = 1
    return M

def monotone_circuit_width(M):
    m, n = len(M), len(M[0])
    dp = [float('inf')] * (n + 1)
    dp[0] = 0
    for i in range(m):
        new_dp = [float('inf')] * (n + 1)
        for j in range(n + 1):
            if dp[j] < float('inf'):
                for k in range(n):
                    if M[i][k]:
                        new_dp[min(j + 1, k + 1)] = min(new_dp[min(j + 1, k + 1)], dp[j] + 1)
        dp = new_dp
    return min(dp[1:])

def run_trial(seed: int) -> dict:
    random.seed(seed)
    q_values = [2**k for k in range(1, 5)]
    results = []
    for q in q_values:
        points, lines = generate_projective_plane(q)
        M = incidence_matrix(points, lines)
        width = monotone_circuit_width(M)
        if width < q**2 + q + 1:
            return {
                "metric_name": "ABP Width",
                "metric_value": width,
                "instances_tested": len(lines),
                "conjecture_holds": False,
                "counterexample": f"q={q}, expected {q**2+q+1}, got {width}"
            }
        results.append(width)
    return {
        "metric_name": "ABP Width",
        "metric_value": sum(results) / len(results),
        "instances_tested": len(lines) * len(q_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or generate_primes(30)
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean_width = sum(results) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_width} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        first_failing_seed = seeds[next(i for i, r in enumerate(results) if not r["conjecture_holds"])]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")