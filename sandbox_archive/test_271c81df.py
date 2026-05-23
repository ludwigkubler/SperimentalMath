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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = 0
    for i in range(n):
        submatrix = [row[:i] + row[i+1:] for row in A[1:]]
        det += (-1) ** i * A[0][i] * determinant(submatrix)
    return det

def coxeter_matrix_invariant(G):
    n = len(G)
    I = [[int(i == j) for j in range(n)] for i in range(n)]
    M = matrix_multiply(I, G)
    M = gaussian_elimination(M)
    det = determinant(M)
    return abs(det)

def read_twice_bp_size(bp):
    return sum(len(layer) for layer in bp)

def generate_read_twice_bp(n):
    bp = []
    for i in range(2):
        layer = [random.randint(0, 1) for _ in range(n)]
        bp.append(layer)
    return bp

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    log_sizes = []
    rho_Gs = []

    for n in n_values:
        bp = generate_read_twice_bp(n)
        G = [[bp[0][i] ^ bp[1][i] for i in range(n)] for _ in range(n)]
        rho_G = coxeter_matrix_invariant(G)
        log_size = math.log(read_twice_bp_size(bp))
        
        log_sizes.append(log_size)
        rho_Gs.append(rho_G)

    metric_value = sum(rho_G * log_size for rho_G, log_size in zip(rho_Gs, log_sizes)) / sum(log_sizes)
    instances_tested = len(n_values)
    
    if any(rho_G > 10 * log_size for rho_G, log_size in zip(rho_Gs, log_sizes)):
        conjecture_holds = False
        counterexample = "rho(G) > 10 * log(size(P))"
    elif all(0.5 <= rho_G / log_size <= 2.0 for rho_G, log_size in zip(rho_Gs, log_sizes)):
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "non-trivial relationship"

    return {
        "metric_name": "Coxeter Matrix Invariant vs BP_ReadTwice Circuit Size",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.2f} std={std_metric_value:.2f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results) and all(r["metric_value"] <= 10 * math.log(read_twice_bp_size(generate_read_twice_bp(40))) for r in results):
        print(f"RESULT: FALSIFIED counterexample=\"non-trivial relationship\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE reason=unsatisfactory_results")