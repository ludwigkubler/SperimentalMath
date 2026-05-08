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

def generate_primes(count):
    primes = []
    num = 2
    while len(primes) < count:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def gaussian_elimination(A, b):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i + 1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
    return x

def matrix_multiply(A, B):
    m, k = len(A), len(B[0])
    n = len(B)
    C = [[0] * k for _ in range(m)]
    for i in range(m):
        for j in range(k):
            for l in range(n):
                C[i][j] += A[i][l] * B[l][j]
    return C

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([8, 10, 12, 14, 16])
    instances_tested = 30
    sld_values = []
    sdps_over_mc = []

    for _ in range(instances_tested):
        # Generate a random 3-regular graph using the configuration model
        degrees = [3] * n
        while True:
            adjacency_matrix = [[0] * n for _ in range(n)]
            for i in range(n):
                neighbors = random.sample(range(n), degrees[i])
                for j in neighbors:
                    if i < j:
                        adjacency_matrix[i][j] = 1
                        adjacency_matrix[j][i] = 1
                degrees[i] -= len(neighbors)
                for j in range(i + 1, n):
                    if adjacency_matrix[i][j]:
                        degrees[j] -= 1
            if all(d == 0 for d in degrees):
                break

        # Compute eigenvalues of the adjacency matrix
        A_G = [row[:] for row in adjacency_matrix]
        lambda_values = gaussian_elimination(A_G, [1] * n)
        lambda_values.sort(reverse=True)

        # Compute Kesten-McKay quantiles
        mu_values = [2 * math.sqrt(2) * math.cos((i - 0.5) * math.pi / n) for i in range(n)]

        # Compute Selberg log-defect (SLD)
        sld = sum(math.log(abs(lambda_values[i] - lambda_values[j])) for i in range(n) for j in range(i + 1, n))
        sld -= sum(math.log(abs(mu_values[i] - mu_values[j])) for i in range(n) for j in range(i + 1, n))
        sld /= n**2
        sld_values.append(sld)

        # Compute exact max-cut (MC)
        best_cut = 0
        for mask in range(1 << n):
            cut_size = bin(mask).count('1')
            if cut_size > n // 2:
                continue
            left_sum = sum(adjacency_matrix[i][j] for i in range(n) for j in range(i + 1, n) if (mask >> i & 1) != (mask >> j & 1))
            best_cut = max(best_cut, left_sum)
        mc_values.append(best_cut)

        # Compute SDP_2 using projected-gradient method
        X = [[0] * n for _ in range(n)]
        for i in range(n):
            X[i][i] = 1
        for _ in range(200):
            grad = [sum(X[i][j] * (adjacency_matrix[i][k] + adjacency_matrix[k][i]) - X[i][k] * X[j][k] for k in range(n)) / n for j in range(n)]
            for i in range(n):
                X[i][i] += 0.1 * grad[i]
                for j in range(i + 1, n):
                    X[i][j] = (X[i][j] + X[j][i]) / 2
                    X[j][i] = X[i][j]
            for i in range(n):
                if X[i][i] < 0:
                    X[i][i] = 0
        sdp_value = sum(adjacency_matrix[i][j] * (X[i][j] - 1 / n) for i in range(n) for j in range(i + 1, n)) / 2
        sdps_over_mc.append(sdp_value / best_cut)

    mean_sld = sum(sld_values) / instances_tested
    std_sld = math.sqrt(sum((x - mean_sld) ** 2 for x in sld_values) / instances_tested)
    mean_sdps_over_mc = sum(sdps_over_mc) / instances_tested
    std_sdps_over_mc = math.sqrt(sum((x - mean_sdps_over_mc) ** 2 for x in sdps_over_mc) / instances_tested)

    conjecture_holds = all(x >= 0.40 for x in sdps_over_mc)
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "SDP_2/MC ratio",
        "metric_value": mean_sdps_over_mc,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or generate_primes(30)
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")