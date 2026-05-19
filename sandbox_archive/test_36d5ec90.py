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
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            if pivot == 0:
                continue
            for j in range(i, n):
                A[i][j] /= pivot
            for j in range(n):
                if j != i and A[j][i] != 0:
                    factor = A[j][i]
                    for k in range(i, n):
                        A[j][k] -= factor * A[i][k]

    def determinant(A):
        n = len(A)
        det = 1
        for i in range(n):
            det *= A[i][i]
        return det

    def log2_floor(x):
        if x <= 0:
            return -math.inf
        return int(math.log2(x))

    def linial_shraibman_gamma(M):
        n = len(M)
        M_T_M = [[sum(M[i][k] * M[j][k] for k in range(n)) for j in range(n)] for i in range(n)]
        v = [random.random() for _ in range(n)]
        for _ in range(20):
            v = [M_T_M[i][j] * v[j] for j in range(n)]
        return math.sqrt(sum(v[i]**2 for i in range(n))) / n

    def generate_sign_matrix(n, family):
        if family == 'uniform':
            return [[random.choice([-1, 1]) for _ in range(n)] for _ in range(n)]
        elif family == 'sylvester_hadamard':
            k = int(math.log2(n))
            M = [[0] * n for _ in range(n)]
            for i in range(k):
                for j in range(k):
                    M[2*i][2*j] = -1
                    M[2*i+1][2*j+1] = 1
            for i in range(n):
                for j in range(n):
                    if i >= k or j >= k:
                        M[i][j] = random.choice([-1, 1])
            return M
        elif family == 'ip_k':
            k = int(math.log2(n))
            M = [[0] * n for _ in range(n)]
            for i in range(k):
                for j in range(k):
                    if i != j:
                        M[2*i][2*j+1] = 1
                        M[2*j][2*i+1] = -1
            return M

    def lambda_2(M):
        n = len(M)
        A = [[0] * (n * math.ceil(math.log2(n))) for _ in range(n)]
        for i in range(n):
            for j in range(n):
                A[i][j * math.ceil(math.log2(n)) + j % math.ceil(math.log2(n))] = M[i][j]
        gaussian_elimination(A)
        det = determinant(A)
        return log2_floor(abs(det))

    def gamma_2(M):
        n = len(M)
        v = [random.random() for _ in range(n)]
        for _ in range(500):
            v = [M[i][j] * v[j] for j in range(n) for i in random.sample(range(n), 2)]
        return math.sqrt(sum(v[i]**2 for i in range(n))) / n

    def rho(M):
        det = determinant(M)
        if det == 0:
            return -math.inf
        return log2_floor(abs(det)) / len(M)

    def run_family(n, family):
        instances_tested = 0
        max_delta = -math.inf
        for _ in range(10):  # Sample 10 instances per family
            M = generate_sign_matrix(n, family)
            g = linial_shraibman_gamma(M)
            rho_M = rho(M)
            delta = rho_M * math.log2(n) - 4 * log2_floor(g)
            if delta > max_delta:
                max_delta = delta
            instances_tested += 1
        return instances_tested, max_delta

    seed = random.seed(seed)
    n_values = [8, 12, 16, 20, 24, 32, 40]
    instances_tested_total = 0
    max_delta_total = -math.inf

    for n in n_values:
        instances_tested_family_a, max_delta_a = run_family(n, 'uniform')
        instances_tested_family_b, max_delta_b = run_family(n, 'sylvester_hadamard')
        instances_tested_family_c, max_delta_c = run_family(n, 'ip_k')
        instances_tested_total += instances_tested_family_a + instances_tested_family_b + instances_tested_family_c
        if max_delta_a > max_delta_total:
            max_delta_total = max_delta_a
        if max_delta_b > max_delta_total:
            max_delta_total = max_delta_b
        if max_delta_c > max_delta_total:
            max_delta_total = max_delta_c

    return {
        "metric_name": "max_delta",
        "metric_value": max_delta_total,
        "instances_tested": instances_tested_total,
        "conjecture_holds": max_delta_total <= 0,
        "counterexample": "" if max_delta_total <= 0 else f"max_delta={max_delta_total} > 0"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    results = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["metric_value"] > 0.5 for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if r["metric_value"] > 0.5)
        print(f"RESULT: FALSIFIED counterexample=\"max_delta>0.5\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")