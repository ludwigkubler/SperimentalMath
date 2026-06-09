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
    random.seed(seed)
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            for j in range(i, n + 1):
                A[i][j] /= pivot
            for j in range(n):
                if j != i:
                    factor = A[j][i]
                    for k in range(i, n + 1):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiplication(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def is_invertible(A):
        det = 1
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            det *= A[i][i]
        return det != 0

    def quadratic_form_count(n):
        count = 0
        for i in range(1 << n):
            Q = [[0] * n for _ in range(n)]
            for j in range(n):
                for k in range(j, n):
                    if (i >> j) & 1 and (i >> k) & 1:
                        Q[j][k] = random.choice([-1, 1])
                        Q[k][j] = Q[j][k]
            if is_invertible(Q):
                count += 1
        return count

    def minimal_representation_degree(n):
        A = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        B = gaussian_elimination(A)
        rank = sum(1 for row in B if any(row))
        return rank

    n_values = [5, 10, 15, 20, 30, 40]
    D_S = []
    q_phi = []

    for n in n_values:
        for _ in range(5):
            D_S.append(minimal_representation_degree(n))
            q_phi.append(quadratic_form_count(n))

    if not D_S or not q_phi:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    mean_D_S = sum(D_S) / len(D_S)
    mean_q_phi = sum(q_phi) / len(q_phi)

    correlation_coefficient = (sum((D_S[i] - mean_D_S) * (q_phi[i] - mean_q_phi) for i in range(len(D_S))) /
                               math.sqrt(sum((D_S[i] - mean_D_S) ** 2 for i in range(len(D_S))) *
                                         sum((q_phi[i] - mean_q_phi) ** 2 for i in range(len(q_phi)))))

    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(D_S),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7 and all(corr >= 0.5 for corr in [correlation_coefficient]),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)

    mean_metric_value = sum(r['metric_value'] for r in results if r['metric_value'] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r['metric_value'] - mean_metric_value) ** 2 for r in results if r['metric_value'] is not None)) / len(results)
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)

    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] and r['metric_value'] < 0.5 for r in results):
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'] and r['metric_value'] < 0.5)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_below_0.5\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")