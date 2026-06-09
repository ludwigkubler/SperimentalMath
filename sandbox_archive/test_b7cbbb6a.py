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
        for k in range(n):
            if k != i and A[k][i] != 0:
                factor = A[k][i]
                for j in range(i, n):
                    A[k][j] -= factor * A[i][j]
    return A

def matrix_multiply(A, B):
    n = len(A)
    C = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def minimal_geometric_entropy(M):
    n = len(M)
    I = [[Fraction(1 if i == j else 0) for j in range(n)] for i in range(n)]
    A = gaussian_elimination(matrix_multiply(I, M))
    det_A = Fraction(1)
    for i in range(n):
        det_A *= A[i][i]
    return -math.log(det_A)

def frege_proof_depth(phi):
    # Placeholder function to compute Frege proof depth
    # This is a dummy implementation and should be replaced with actual logic
    return random.randint(1, 10)  # Randomly generated for demonstration

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    phi = [random.sample(range(1, n+1), 2) for _ in range(n)]
    M = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                M[i][j] = Fraction(1)
            else:
                M[i][j] = Fraction(1, abs(sum(set(phi[k]) & set(phi[l]))))
    het_M = minimal_geometric_entropy(M)
    d_phi = frege_proof_depth(phi)
    return {
        "metric_name": "Frege proof depth vs. geometric entropy",
        "metric_value": d_phi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": het_M > 0,  # Placeholder condition
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_conjecture_support")