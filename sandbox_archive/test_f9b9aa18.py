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
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]

def determinant(A):
    n = len(A)
    det = Fraction(1)
    for i in range(n):
        det *= A[i][i]
    return det

def trace(matrix):
    n = len(matrix)
    tr = 0
    for i in range(n):
        tr += matrix[i][i]
    return tr

def unitary_matrix(n):
    U = [[Fraction(0, 1)] * n for _ in range(n)]
    for i in range(n):
        U[i][i] = Fraction(1, 1)
    return U

def frobenius_schur_indicator(U, n):
    n = len(U)
    identity = unitary_matrix(n)
    result = trace(matrix_multiplication(identity, U.conjugate().transpose())) / math.factorial(n)
    return abs(result)

def matrix_multiplication(A, B):
    n = len(A)
    C = [[Fraction(0, 1)] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def entropy(distribution):
    H = Fraction(0, 1)
    for p in distribution:
        if p > 0:
            H -= p * math.log2(p)
    return H

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    U = unitary_matrix(n)
    distribution = [random.random() for _ in range(2**n)]
    total = sum(distribution)
    distribution = [p / total for p in distribution]
    
    metric_value = frobenius_schur_indicator(U, n)
    entropy_value = entropy(distribution)
    
    conjecture_holds = abs(metric_value) <= entropy_value
    counterexample = "" if conjecture_holds else "Frobenius-Schur Indicator > Entropy"
    
    return {
        "metric_name": "Frobenius-Schur Indicator",
        "metric_value": metric_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
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
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Frobenius-Schur Indicator > Entropy\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")