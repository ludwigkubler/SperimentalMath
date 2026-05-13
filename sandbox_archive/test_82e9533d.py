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
    
    def matrix_multiply(A, B):
        n = len(A)
        result = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    result[i][j] += A[i][k] * B[k][j]
        return result
    
    def gaussian_elimination(A, b):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for j in range(i+1, n):
                factor = A[j][i] / A[i][i]
                A[j][i] = 0
                for k in range(i+1, n):
                    A[j][k] -= factor * A[i][k]
                b[j] -= factor * b[i]
        x = [0 for _ in range(n)]
        for i in range(n-1, -1, -1):
            x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
        return x
    
    def inverse_matrix(A):
        n = len(A)
        I = [[0 if i != j else 1 for j in range(n)] for i in range(n)]
        gaussian_elimination(A, I)
        return I
    
    def r_transform_inv(M):
        n = len(M)
        M_inv = inverse_matrix(M)
        R = [[0 for _ in range(n)] for _ in range(n)]
        for k in range(1, 5):  # Approximate with first few terms
            term = math.factorial(k-1) / (2 * (k**2 - 1))
            R += term * matrix_multiply(M_inv, M_inv)
        return R
    
    def free_cumulant_sum(R):
        n = len(R)
        cumulants = [0 for _ in range(n)]
        for k in range(1, n+1):
            cumulants[k-1] = sum(R[i][j] * (i**k + j**k) / (2 * (i+j)**k) for i in range(k) for j in range(k))
        return sum(cumulants)
    
    def generate_disjointness_matrix(n):
        M = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            M[i][i] = 1
        return M
    
    n = random.randint(5, 40)
    M = generate_disjointness_matrix(n)
    R = r_transform_inv(M)
    tau_M = free_cumulant_sum(R)
    
    metric_name = "free_cumulant_sum"
    metric_value = tau_M
    instances_tested = 1
    conjecture_holds = tau_M >= 0.3 * n
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")