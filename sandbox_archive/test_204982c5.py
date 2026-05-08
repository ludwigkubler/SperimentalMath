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
    C = [[0 for _ in range(k)] for _ in range(m)]
    for i in range(m):
        for j in range(k):
            for l in range(n):
                C[i][j] += A[i][l] * B[l][j]
    return C

def transpose(A):
    m, n = len(A), len(A[0])
    B = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(m):
        for j in range(n):
            B[j][i] = A[i][j]
    return B

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    rref = [[A[i][j] for j in range(n)] for i in range(m)]
    lead = 0
    for r in range(m):
        if lead >= n:
            break
        i = r
        while rref[i][lead] == 0:
            i += 1
            if i == m:
                i = r
                lead += 1
                if lead == n:
                    break
        rref[r], rref[i] = rref[i], rref[r]
        factor = rref[r][lead]
        for j in range(n):
            rref[r][j] /= factor
        for i in range(m):
            if i != r and rref[i][lead]:
                factor = rref[i][lead]
                for j in range(n):
                    rref[i][j] -= factor * rref[r][j]
        lead += 1
    return rref

def rank(A):
    rref = gaussian_elimination(A)
    rank = sum(1 for row in rref if any(row))
    return rank

def secant_variety_dimension(M):
    m, n = len(M), len(M[0])
    rank_M = rank(M)
    if rank_M == 1:
        return 1
    A_augmented = [[M[i][j] for j in range(n)] + [1] for i in range(m)]
    rref_A_augmented = gaussian_elimination(A_augmented)
    k = len(rref_A_augmented[0]) - 1
    tau_M = m * n - rank_M * (k - 1) - rank_M
    return tau_M

def disjointness_matrix(n):
    M = [[0 for _ in range(2**n)] for _ in range(2**n)]
    for i in range(2**n):
        for j in range(2**n):
            if (i & j) == 0:
                M[i][j] = 1
    return M

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        M = disjointness_matrix(n)
        tau_M = secant_variety_dimension(M)
        if tau_M < n / 2:
            return {
                "metric_name": "secant_variety_dimension",
                "metric_value": tau_M,
                "instances_tested": len(n_values),
                "conjecture_holds": False,
                "counterexample": f"n={n}, tau(M)={tau_M}"
            }
        results.append(tau_M)
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    return {
        "metric_name": "secant_variety_dimension",
        "metric_value": mean,
        "instances_tested": len(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        seeds = primes[:30]
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
    mean = sum(result['metric_value'] for result in results) / len(results)
    std = math.sqrt(sum((result['metric_value'] - mean) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result['conjecture_holds']) / len(results)
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not result['conjecture_holds'] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")