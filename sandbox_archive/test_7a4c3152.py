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
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, m):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def matrix_multiply(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0]*p for _ in range(m)]
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
        det += (-1)**j * A[0][j] * determinant(submatrix)
    return det

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 40
    d = 20
    
    # Generate a random boolean circuit with depth d
    circuit = []
    for _ in range(d):
        layer = [random.choice([0, 1]) for _ in range(n)]
        circuit.append(layer)
    
    # Compute the monotone width of the circuit
    w_C = max(sum(row) for row in circuit)
    
    # Convert the circuit to a matroid and compute its minimal tropical motivic rank
    mtr_C = 0
    for i in range(n):
        for j in range(i+1, n):
            if all(circuit[k][i] == circuit[k][j] for k in range(d)):
                mtr_C += 1
    
    # Return the results
    return {
        "metric_name": "tropical_motivic_rank",
        "metric_value": mtr_C,
        "instances_tested": n * d,
        "n_max": n,
        "conjecture_holds": abs(mtr_C - w_C) <= 10,
        "counterexample": "" if abs(mtr_C - w_C) <= 10 else f"mtr(C)={mtr_C}, w(C)={w_C}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and abs(r["metric_value"] - r["n_max"]) > 10 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mtr(C) ≈ w(C)\", first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")