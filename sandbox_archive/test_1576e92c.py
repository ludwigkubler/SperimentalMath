# auto-injected by SEC sandbox
import itertools
import collections
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import json

def matrix_multiply(A, B):
    n = len(A)
    m = len(B[0])
    p = len(B)
    result = [[0.0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            for k in range(p):
                result[i][j] += A[i][k] * B[k][j]
    return result

def transpose(matrix):
    return [list(row) for row in zip(*matrix)]

def svd(matrix):
    n = len(matrix)
    m = len(matrix[0])
    A = [[float(x) for x in row] for row in matrix]
    ATA = matrix_multiply(transpose(A), A)
    s = [0.0] * min(n, m)
    for i in range(min(n, m)):
        if i >= len(ATA) or i >= len(ATA[0]):
            continue
        s[i] = math.sqrt(ATA[i][i]) if ATA[i][i] >= 0 else 0.0
    return None, s, None

def compute_spectral_excess(M_tilde, k, seed):
    random.seed(seed)
    N = len(M_tilde)
    xi = 0.0
    instances = 0
    for _ in range(30):
        S = sorted(random.sample(range(N), k))
        submatrix = [[M_tilde[i][j] for j in S] for i in range(N)]
        _, s, _ = svd(submatrix)
        if not s:
            continue
        op_norm_sq = s[0] ** 2 if s else 0.0
        xi += (op_norm_sq / N - 1)
        instances += 1
    xi /= 30 if instances > 0 else 1
    return xi, instances

def construct_disj_matrix(n):
    N = 2 ** n
    M = [[0] * N for _ in range(N)]
    for x in range(N):
        for y in range(N):
            M[x][y] = 1 if not (x & y) else 0
    return M

def construct_parity_matrix(n):
    N = 2 ** n
    M = [[0] * N for _ in range(N)]
    for x in range(N):
        for y in range(N):
            M[x][y] = (1 + (-1) ** bin(x & y).count('1')) // 2
    return M

def construct_random_matrix(n):
    N = 2 ** n
    M = [[0] * N for _ in range(N)]
    for x in range(N):
        for y in range(N):
            M[x][y] = random.randint(0, 1)
    return M

def center_matrix(M):
    N = len(M)
    row_sums = [sum(row) for row in M]
    col_sums = [sum(M[i][j] for i in range(N)) for j in range(N)]
    total_sum = sum(row_sums)
    M_tilde = [[0] * N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            M_tilde[i][j] = 2 * M[i][j] - row_sums[i] - col_sums[j] + total_sum / N
    return M_tilde

def run_trial(seed):
    n_values = [3, 4, 5]
    results = []
    for n in n_values:
        N = 2 ** n
        k = math.ceil(math.log2(N))

        # Construct and center DISJ matrix
        M_disj = construct_disj_matrix(n)
        M_disj_tilde = center_matrix(M_disj)
        xi_disj, instances_disj = compute_spectral_excess(M_disj_tilde, k, seed)

        # Construct and center PARITY matrix
        M_parity = construct_parity_matrix(n)
        M_parity_tilde = center_matrix(M_parity)
        xi_parity, instances_parity = compute_spectral_excess(M_parity_tilde, k, seed)

        # Construct and center random matrix
        M_random = construct_random_matrix(n)
        M_random_tilde = center_matrix(M_random)
        xi_random, instances_random = compute_spectral_excess(M_random_tilde, k, seed)

        # Check conditions
        condition1 = xi_disj >= 0.5 * k / n
        condition2 = xi_parity <= 0.05
        condition3 = xi_random <= 0.3 * k / N

        conjecture_holds = condition1 and condition2 and condition3
        counterexample = ""
        if not condition1:
            counterexample = f"xi_disj={xi_disj} < 0.5*k/n={0.5*k/n}"
        elif not condition2:
            counterexample = f"xi_parity={xi_parity} > 0.05"
        elif not condition3:
            counterexample = f"xi_random={xi_random} > 0.3*k/N={0.3*k/N}"

        results.append({
            "n": n,
            "xi_disj": xi_disj,
            "xi_parity": xi_parity,
            "xi_random": xi_random,
            "instances_tested": instances_disj + instances_parity + instances_random,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        })

    # Aggregate results
    metric_values = [r["xi_disj"] for r in results]
    metric_value = sum(metric_values) / len(metric_values) if metric_values else 0.0
    instances_tested = sum(r["instances_tested"] for r in results)
    conjecture_holds = all(r["conjecture_holds"] for r in results)
    counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")

    return {
        "metric_name": "xi_disj",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    trials = []
    for seed in seeds:
        result = run_trial(seed)
        trials.append({"seed": seed, **result})
        print(f"TRIAL: {json.dumps({'seed': seed, **result})}")

    metric_values = [trial["metric_value"] for trial in trials]
    mean_metric = sum(metric_values) / len(metric_values) if metric_values else 0.0
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values)) if metric_values else 0.0
    support_fraction = sum(1 for trial in trials if trial["conjecture_holds"]) / len(trials) if trials else 0.0

    if all(trial["conjecture_holds"] for trial in trials):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not trial["conjecture_holds"] for trial in trials):
        first_failing_seed = next(trial["seed"] for trial in trials if not trial["conjecture_holds"])
        counterexample = next(trial["counterexample"] for trial in trials if not trial["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=all_trials_failed")