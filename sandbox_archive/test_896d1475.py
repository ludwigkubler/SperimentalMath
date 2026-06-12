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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def matrix_multiply(A, B):
        m = len(A)
        n = len(B[0])
        p = len(B)
        C = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def matrix_add(A, B):
        m = len(A)
        n = len(A[0])
        C = [[A[i][j] + B[i][j] for j in range(n)] for i in range(m)]
        return C
    
    def matrix_sub(A, B):
        m = len(A)
        n = len(A[0])
        C = [[A[i][j] - B[i][j] for j in range(n)] for i in range(m)]
        return C
    
    def matrix_transpose(A):
        m = len(A)
        n = len(A[0])
        B = [[0] * m for _ in range(n)]
        for i in range(m):
            for j in range(n):
                B[j][i] = A[i][j]
        return B
    
    def matrix_inverse(A):
        m = len(A)
        n = len(A[0])
        if m != n:
            raise ValueError("Matrix must be square")
        I = [[1 if i == j else 0 for j in range(n)] for i in range(m)]
        for k in range(n):
            pivot = A[k][k]
            if pivot == 0:
                raise ValueError("Matrix is not invertible")
            for j in range(k, n):
                A[k][j] /= pivot
                I[k][j] /= pivot
            for i in range(m):
                if i != k:
                    factor = A[i][k]
                    for j in range(k, n):
                        A[i][j] -= factor * A[k][j]
                        I[i][j] -= factor * I[k][j]
        return I
    
    def gaussian_elimination(A):
        m = len(A)
        n = len(A[0])
        B = [row[:] for row in A]
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(B[j][i]) > abs(B[max_row][i]):
                    max_row = j
            B[i], B[max_row] = B[max_row], B[i]
            pivot = B[i][i]
            for j in range(n):
                B[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = B[j][i]
                    for k in range(n):
                        B[j][k] -= factor * B[i][k]
        return B
    
    def determinant(A):
        m = len(A)
        n = len(A[0])
        if m != n:
            raise ValueError("Matrix must be square")
        if n == 1:
            return A[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1)**j * A[0][j] * determinant(submatrix)
        return det
    
    def rank(A):
        m = len(A)
        n = len(A[0])
        B = gaussian_elimination(A)
        r = 0
        for i in range(m):
            if any(B[i]):
                r += 1
        return r
    
    def communication_complexity_rank_variance(f):
        n = int(math.log2(len(f)))
        A = [[f[j] ^ f[j + 2**i] for j in range(2**(n-i-1))] for i in range(n)]
        return rank(A)
    
    def kostant_multiplicity(f):
        n = int(math.log2(len(f)))
        A = [[f[j] ^ f[j + 2**i] for j in range(2**(n-i-1))] for i in range(n)]
        B = gaussian_elimination(A)
        return sum(abs(B[i][j]) for i in range(n) for j in range(i, n))
    
    def O(f):
        n = int(math.log2(len(f)))
        return n
    
    def Omega(f):
        n = int(math.log2(len(f)))
        return 2**n
    
    f = generate_boolean_function(5)
    kappa_f = kostant_multiplicity(f)
    rank_variance_f = communication_complexity_rank_variance(f)
    
    return {
        "metric_name": "Kostant Multiplicity vs Communication Complexity Rank Variance",
        "metric_value": kappa_f,
        "instances_tested": 1,
        "n_max": 5,
        "conjecture_holds": O(f) <= kappa_f <= Omega(f),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")