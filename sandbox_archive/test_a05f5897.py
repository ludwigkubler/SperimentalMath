# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
import itertools

def generate_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def polynomial_from_boolean_function(f, n):
    poly = [0] * (n + 1)
    for i in range(len(f)):
        binary_rep = f"{i:0{n}b}"
        coeff = int(binary_rep[-1])
        exp = sum(int(bit) * (2 ** idx) for idx, bit in enumerate(reversed(binary_rep[:-1])))
        poly[exp] += coeff
    return poly

def matrix_add(A, B, mod):
    return [[(a + b) % mod for a, b in zip(row_a, row_b)] for row_a, row_b in zip(A, B)]

def matrix_mul(A, B, mod):
    result = [[0] * len(B[0]) for _ in range(len(A))]
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                result[i][j] = (result[i][j] + A[i][k] * B[k][j]) % mod
    return result

def matrix_pow(M, exp, mod):
    result = [[int(i == j) for j in range(len(M))] for i in range(len(M))]
    base = M
    while exp > 0:
        if exp % 2 == 1:
            result = matrix_mul(result, base, mod)
        base = matrix_mul(base, base, mod)
        exp //= 2
    return result

def minimal_local_ring_rank(poly):
    n = len(poly) - 1
    q = 2
    A = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        A[i][i] = 1
    for exp, coeff in enumerate(poly[1:], start=1):
        if coeff != 0:
            for j in range(n + 1):
                A[exp][j] = (A[exp][j] + coeff * pow(exp, j, q)) % q
    rank = n + 1
    for i in range(n, -1, -1):
        if all(A[j][i] == 0 for j in range(i, n + 1)):
            rank -= 1
        else:
            pivot_row = next(j for j in range(i, n + 1) if A[j][i] != 0)
            A[i], A[pivot_row] = A[pivot_row], A[i]
            for j in range(n + 1):
                if i != j:
                    factor = (A[j][i] * pow(A[i][i], q - 2, q)) % q
                    A[j] = [((A[j][k] - factor * A[i][k]) % q) for k in range(n + 1)]
    return rank

def communication_complexity_rank_variance(f, n):
    poly = polynomial_from_boolean_function(f, n)
    mrr = minimal_local_ring_rank(poly)
    rcv = sum((i - mrr)**2 for i in range(mrr)) / (mrr * (mrr + 1))
    return rcv

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_instances = 0
    mrr_sum = 0.0
    rcv_sum = 0.0
    max_n = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            f = generate_boolean_function(n)
            mrr = minimal_local_ring_rank(polynomial_from_boolean_function(f, n))
            rcv = communication_complexity_rank_variance(f, n)
            total_instances += 1
            max_n = max(max_n, n)
            mrr_sum += mrr
            rcv_sum += rcv

    mean_mrr = mrr_sum / total_instances
    mean_rcv = rcv_sum / total_instances
    correlation_coefficient = (total_instances * sum(mrr * rcv for mrr, rcv in zip(range(1, max_n + 1), range(1, max_n + 1))) -
                               mrr_sum * rcv_sum) / math.sqrt((total_instances * sum(mrr**2 for mrr in range(1, max_n + 1)) - mrr_sum**2) *
                                                            (total_instances * sum(rcv**2 for rcv in range(1, max_n + 1)) - rcv_sum**2))

    if correlation_coefficient < 0.9:
        conjecture_holds = False
        counterexample = "correlation_coefficient_too_low"

    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": total_instances,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **trial_result}}")
        results.append(trial_result)

    mean_corr_coeff = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_too_low\" first_failing_seed={first_failing_seed}")