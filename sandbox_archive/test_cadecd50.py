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

def generate_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def polynomial_representation(f, n):
    q = 2
    poly = []
    for i in range(n + 1):
        coeff = sum(f[j] * (i & (1 << j)) for j in range(n)) % q
        if coeff != 0:
            poly.append((coeff, i))
    return poly

def matrix_mult(A, B, mod):
    m, k = len(A), len(B[0])
    n = len(B)
    C = [[0] * k for _ in range(m)]
    for i in range(m):
        for j in range(k):
            for l in range(n):
                C[i][j] = (C[i][j] + A[i][l] * B[l][j]) % mod
    return C

def matrix_sub(A, B, mod):
    m, n = len(A), len(A[0])
    C = [[(A[i][j] - B[i][j]) % mod for j in range(n)] for i in range(m)]
    return C

def gaussian_elimination(M, mod):
    m, n = len(M), len(M[0])
    rank = 0
    for col in range(n):
        pivot_row = None
        for row in range(rank, m):
            if M[row][col] != 0:
                pivot_row = row
                break
        if pivot_row is not None:
            M[pivot_row], M[rank] = M[rank], M[pivot_row]
            for r in range(m):
                if r != rank and M[r][col] != 0:
                    factor = -M[r][col] * pow(M[pivot_row][col], mod-2, mod) % mod
                    M[r] = matrix_add(matrix_mul([[factor]], M[pivot_row], mod), M[r], mod)
            rank += 1
    return rank

def minimal_local_ring_rank(poly):
    q = 2
    n = len(poly)
    A = [[0] * (n + 1) for _ in range(n + 1)]
    for coeff, exp in poly:
        for j in range(n + 1):
            A[exp][j] = (A[exp][j] + coeff * pow(exp, j, q)) % q
    return gaussian_elimination(A, q)

def communication_complexity_rank_variance(f, n):
    q = 2
    poly = polynomial_representation(f, n)
    rank = minimal_local_ring_rank(poly)
    return (rank - n) ** 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        f = generate_boolean_function(n)
        rcv = communication_complexity_rank_variance(f, n)
        mrr = minimal_local_ring_rank(polynomial_representation(f, n))
        results.append((n, rcv, mrr))
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_results"
        }
    
    n_values, rcv_values, mrr_values = zip(*results)
    mean_rcv = sum(rcv_values) / len(rcv_values)
    mean_mrr = sum(mrr_values) / len(mrr_values)
    correlation_coefficient = sum((rcv - mean_rcv) * (mrr - mean_mrr) for rcv, mrr in zip(rcv_values, mrr_values)) / (len(rcv_values) * math.sqrt(sum((rcv - mean_rcv) ** 2 for rcv in rcv_values) * sum((mrr - mean_mrr) ** 2 for mrr in mrr_values)))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": 0.9 <= abs(correlation_coefficient) <= 1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results if result["metric_value"] is not None)) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_outside_0.9_to_1\" first_failing_seed={result['seed']}")
                break