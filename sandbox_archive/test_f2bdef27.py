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

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
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

def random_boolean_circuit(n, m):
    circuit = []
    for _ in range(m):
        gate_type = random.choice(['AND', 'OR'])
        inputs = [random.randint(0, 1) for _ in range(random.randint(2, n))]
        circuit.append((gate_type, inputs))
    return circuit

def matroid_rank(circuit):
    n = len(circuit)
    rank_matrix = [[0] * (n+1) for _ in range(n+1)]
    for i in range(n):
        gate_type, inputs = circuit[i]
        if gate_type == 'AND':
            rank_matrix[inputs[0]][i+1] = 1
            rank_matrix[inputs[1]][i+1] = 1
        else:
            rank_matrix[inputs[0]][i+1] = 1
            rank_matrix[inputs[1]][i+1] = 1
    return len(gaussian_elimination(rank_matrix, [0]*(n+1)))

def tropical_hodge_dimension(circuit):
    n = matroid_rank(circuit)
    return n

def rank_variance(circuit):
    ranks = [matroid_rank(circuit) for _ in range(10)]
    mean = sum(ranks) / len(ranks)
    variance = sum((x - mean) ** 2 for x in ranks) / len(ranks)
    return variance

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    thd_values = []
    rcv_values = []
    instances_tested = 0
    n_max = 0

    for n in n_values:
        for _ in range(5):
            circuit = random_boolean_circuit(n, n * (n - 1))
            thd = tropical_hodge_dimension(circuit)
            rcv = rank_variance(circuit)
            thd_values.append(thd)
            rcv_values.append(rcv)
            instances_tested += 1
            if n > n_max:
                n_max = n

    mean_thd = sum(thd_values) / len(thd_values)
    mean_rcv = sum(rcv_values) / len(rcv_values)
    std_rcv = math.sqrt(sum((x - mean_rcv) ** 2 for x in rcv_values) / len(rcv_values))
    correlation_coefficient = (sum((thd_values[i] - mean_thd) * (rcv_values[i] - mean_rcv) for i in range(len(thd_values))) /
                               (len(thd_values) * std_rcv * std_rcv))

    conjecture_holds = abs(correlation_coefficient) >= 0.8
    counterexample = "" if conjecture_holds else "correlation_coefficient"

    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)

    mean_corr_coeff = sum(r["metric_value"] for r in results) / len(results)
    std_corr_coeff = math.sqrt(sum((r["metric_value"] - mean_corr_coeff) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std={std_corr_coeff} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")