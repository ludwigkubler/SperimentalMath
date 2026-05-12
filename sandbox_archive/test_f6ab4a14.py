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

def generate_disjointness_matrix(n):
    M = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            M[i][j] = M[j][i] = random.randint(0, 1)
    return M

def matrix_multiply(A, B):
    m, k, n = len(A), len(B[0]), len(B)
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for l in range(k):
                C[i][j] += A[i][l] * B[l][j]
    return C

def transpose(A):
    m, n = len(A), len(A[0])
    T = [[0] * m for _ in range(n)]
    for i in range(m):
        for j in range(n):
            T[j][i] = A[i][j]
    return T

def svd(A):
    U, S, Vt = [], [], []
    A_t = transpose(A)
    Q, R = gram_schmidt(A), gram_schmidt(A_t)
    S = [[sum([A[i][k] * A[j][k] for k in range(len(A))]) if i == j else 0 for j in range(len(A))] for i in range(len(A))]
    U = Q
    Vt = transpose(R)
    return U, S, Vt

def gram_schmidt(A):
    m, n = len(A), len(A[0])
    Q = []
    R = [[0] * n for _ in range(n)]
    for i in range(n):
        v = A[i]
        for j in range(i):
            r_ij = sum([Q[j][k] * v[k] for k in range(m)])
            v = [v[k] - r_ij * Q[j][k] for k in range(m)]
            R[j][i] = r_ij
        r_ii = math.sqrt(sum(v[k]**2 for k in range(m)))
        Q.append([v[k] / r_ii for k in range(m)])
        R[i][i] = r_ii
    return Q

def rank(A):
    U, S, Vt = svd(A)
    return sum(1 for s in S if abs(s) > 1e-6)

def secant_rank(M):
    n = len(M)
    A = M + [M[0]] * (n - 1)
    B = [M[i] for i in range(1, n)]
    C = matrix_multiply(A, transpose(B))
    return rank(C)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        M_n = generate_disjointness_matrix(n)
        sr_M_n = secant_rank(M_n)
        metric_value = sr_M_n / (0.6 * n)
        total_metric_value += metric_value
        instances_tested += 1

        if sr_M_n < 0.6 * n:
            conjecture_holds = False
            counterexample = f"n={n}, sr(M_n)={sr_M_n}"

    return {
        "metric_name": "secant_rank_over_n",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']:.6f}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.6f} std={std_metric_value:.6f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data or too many failures")