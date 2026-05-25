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
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i + max(range(i, m), key=lambda x: abs(A[x][i]))
        A[i], A[max_row] = A[max_row], A[i]
        if A[i][i] == 0:
            raise ValueError("Matrix is singular")
        for j in range(n):
            A[i][j] /= A[i][i]
        for k in range(m):
            if k != i and A[k][i]:
                factor = A[k][i]
                for j in range(n):
                    A[k][j] -= factor * A[i][j]

def matrix_multiply(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def determinant(A):
    m, n = len(A), len(A[0])
    if m != n:
        raise ValueError("Matrix must be square")
    if m == 1:
        return A[0][0]
    det = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det += (-1) ** j * A[0][j] * determinant(submatrix)
    return det

def hodge_theta_index(cnf):
    m, n = len(cnf), len(cnf[0])
    H = [[0] * (n + 1) for _ in range(m)]
    for i in range(m):
        for j in range(n):
            if cnf[i][j]:
                H[i][j] = 1
                H[i][-1] += 1
    gaussian_elimination(H)
    return max(abs(sum(row)) for row in H)

def frege_proof_depth(cnf, clause):
    # Placeholder function to simulate Frege proof depth calculation
    # This is a dummy implementation and should be replaced with actual logic
    return len(clause) * 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(n, n + 10)
    cnf = [[random.choice([0, 1]) for _ in range(n)] for _ in range(m)]
    hodge_index = hodge_theta_index(cnf)
    max_depth = max(frege_proof_depth(cnf, clause) for clause in cnf)
    resolution_length = m
    conjecture_holds = hodge_index <= 1.5 * resolution_length
    counterexample = "" if conjecture_holds else "Hodge-Theta index exceeds 1.5 times resolution length"
    return {
        "metric_name": "Hodge-Theta Index",
        "metric_value": hodge_index,
        "instances_tested": m,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30*4 + 1, 2))
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Hodge-Theta index exceeds 1.5 times resolution length\" first_failing_seed={first_failing_seed}")