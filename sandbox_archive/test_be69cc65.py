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

def gram_schmidt(A):
    n, m = len(A), len(A[0])
    Q = [[Fraction(0) for _ in range(m)] for _ in range(n)]
    R = [[Fraction(0) for _ in range(m)] for _ in range(n)]

    for i in range(n):
        v_i = [A[i][j] for j in range(m)]
        for j in range(i):
            r_ij = sum(Q[j][k] * A[i][k] for k in range(m))
            R[j][i] = r_ij
            for k in range(m):
                v_i[k] -= r_ij * Q[j][k]
        norm_v_i = math.sqrt(sum(v_i[j]**2 for j in range(m)))
        if norm_v_i == 0:
            raise ValueError("Vector is linearly dependent")
        R[i][i] = norm_v_i
        for k in range(m):
            Q[i][k] = v_i[k] / norm_v_i

    return Q, R

def singular_value_decomposition(A):
    n, m = len(A), len(A[0])
    U, S, Vt = [[Fraction(0) for _ in range(n)] for _ in range(n)], \
               [Fraction(0) for _ in range(min(n, m))], \
               [[Fraction(0) for _ in range(m)] for _ in range(m)]

    Q, R = gram_schmidt(A)
    for i in range(n):
        U[i] = Q[i]
    S = [R[i][i] for i in range(min(n, m))]
    Vt = [[Fraction(0) for _ in range(m)] for _ in range(m)]
    for i in range(min(n, m)):
        Vt[i][i] = Fraction(1) / R[i][i]

    return U, S, Vt

def schatten_p_norm(matrix, p):
    if p == 2:
        return sum(x**2 for row in matrix for x in row)**0.5
    elif p == float('inf'):
        return max(sum(abs(x) for x in row) for row in matrix)
    else:
        raise ValueError("Unsupported p value")

def disjointness_instance(n):
    A = [random.randint(0, 1) for _ in range(n)]
    B = [random.randint(0, 1) for _ in range(n)]
    return A, B

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            A, B = disjointness_instance(n)
            communication_matrix = [[A[i] * B[j] for j in range(n)] for i in range(n)]
            norm = schatten_p_norm(communication_matrix, p=2)  # Using p=2 as an example
            total_metric_value += norm
            instances_tested += 1

    mean_metric_value = total_metric_value / instances_tested
    if mean_metric_value < n_values[-1]:
        conjecture_holds = False
        counterexample = "Schatten p-norm does not scale linearly with n"

    return {
        "metric_name": "Schatten p-Norm",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 8)]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")

    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Schatten p-norm does not scale linearly with n\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")