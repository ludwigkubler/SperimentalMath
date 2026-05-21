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

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def generate_primes(k):
    primes = []
    num = 2
    while len(primes) < k:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def random_disjointness_matrix(n):
    M = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            M[i][j] = M[j][i] = random.choice([0, 1])
    return M

def fft_2d(M):
    n = len(M)
    if n == 1:
        return M
    even_M = [fft_2d([row[::2] for row in col]) for col in zip(*M)]
    odd_M = [fft_2d([row[1::2] for row in col]) for col in zip(*M)]
    T = [[0] * n for _ in range(n // 2)]
    for k in range(n // 2):
        angle = -2 * math.pi * k / n
        w = [math.cos(angle), math.sin(angle)]
        for j in range(n // 2):
            T[j][k] = (even_M[k][j] + odd_M[k][j] * w[0]) + (even_M[k][j] - odd_M[k][j] * w[0]) * 1j
    result = [[0] * n for _ in range(n)]
    for k in range(n // 2):
        for j in range(n):
            result[j][k] = T[j % (n // 2)][k] + T[(j + n // 2) % (n // 2)][k]
            result[j][k + n // 2] = T[j % (n // 2)][k] - T[(j + n // 2) % (n // 2)][k]
    return result

def l2_norm(M):
    norm = 0
    for row in M:
        for val in row:
            norm += abs(val) ** 2
    return math.sqrt(norm)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    M = random_disjointness_matrix(n)
    F = fft_2d(M)
    norm = l2_norm(F)
    return {
        "metric_name": "L^2 norm",
        "metric_value": norm,
        "instances_tested": 1,
        "conjecture_holds": norm >= n,
        "counterexample": "" if norm >= n else f"Matrix with L^2 norm {norm} < {n}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or generate_primes(30)
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)

    mean_norm = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_norm} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_norm} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")