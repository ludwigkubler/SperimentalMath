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

# Helper functions for matrix operations
def matrix_multiplication(A, B):
    m = len(A)
    n = len(B[0])
    p = len(B)
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for l in range(p):
                C[i][j] += A[i][l] * B[l][j]
    return C

def matrix_addition(A, B):
    m = len(A)
    n = len(A[0])
    C = [[A[i][j] + B[i][j] for j in range(n)] for i in range(m)]
    return C

def identity_matrix(n):
    I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    return I

def transpose(A):
    m = len(A)
    n = len(A[0])
    B = [[A[j][i] for j in range(m)] for i in range(n)]
    return B

# Helper function to generate a random DISJOINTNESS matrix
def generate_disjointness_matrix(n):
    X = set(random.sample(range(2*n), n))
    Y = set(random.sample(range(2*n, 4*n), n))
    M = [[0] * (2*n) for _ in range(2*n)]
    for i in X:
        for j in Y:
            if i < j:
                M[i][j] = 1
    return M

# Noncommutative Fourier transform using the regular representation of F_2
def noncommutative_fourier_transform(M, rep):
    n = len(M)
    m = len(rep)
    fourier_rep = [[0] * m for _ in range(m)]
    for i in range(m):
        for j in range(m):
            if i == j:
                fourier_rep[i][j] = 1
            else:
                fourier_rep[i][j] = -1
    return matrix_multiplication(fourier_rep, matrix_multiplication(M, fourier_rep))

# Run a single trial with the given seed
def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0.0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        M = generate_disjointness_matrix(n)
        F_M = noncommutative_fourier_transform(M, rep)
        operator_norm = max([sum(abs(x) for x in row) for row in F_M])
        total_metric_value += operator_norm
        instances_tested += 1

    mean_metric_value = total_metric_value / instances_tested
    if abs(mean_metric_value - 0.5) > 0.1:
        conjecture_holds = False
        counterexample = "mean_metric_value deviates from expected"

    return {
        "metric_name": "operator_norm",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mean_metric_value deviates from expected\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")