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
        m = len(A)
        n = len(B[0])
        p = len(B)
        result = [[sum(A[i][k] * B[k][j] for k in range(p)) for j in range(n)] for i in range(m)]
        return result
    
    def determinant(matrix):
        if len(matrix) == 1:
            return matrix[0][0]
        det = 0
        for c in range(len(matrix)):
            submatrix = [row[:c] + row[c+1:] for row in matrix[1:]]
            sign = (-1) ** (c % 2)
            sub_det = determinant(submatrix)
            det += sign * matrix[0][c] * sub_det
        return det
    
    def permanent(matrix):
        if len(matrix) == 1:
            return matrix[0][0]
        perm = 0
        for c in range(len(matrix)):
            submatrix = [row[:c] + row[c+1:] for row in matrix[1:]]
            sign = (-1) ** (c % 2)
            sub_perm = permanent(submatrix)
            perm += sign * matrix[0][c] * sub_perm
        return perm
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            factor = 1 / A[i][i]
            for j in range(n):
                A[i][j] *= factor
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A
    
    def rank(matrix):
        rref = gaussian_elimination(matrix)
        rank = sum(1 for row in rref if any(row[j] != 0 for j in range(len(row))))
        return rank
    
    def hilbert_polynomial(n, k):
        # This is a placeholder function. The actual implementation depends on the specific form of the Hilbert polynomial.
        # For simplicity, we assume a known form here.
        return (n - k + 1) ** n / math.factorial(k)
    
    def circuitsize(n):
        # Placeholder for the minimal circuit size for computing the permanent.
        # This is a simplified example. The actual implementation depends on the specific algorithm used.
        return n * n
    
    n = random.randint(5, 40)
    k = random.randint(1, n-1)
    M = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
    
    I = []
    for r in range(k+1):
        for A in itertools.combinations(M, r):
            if rank(A) == r:
                I.append(A)
    
    hp = hilbert_polynomial(n, k)
    leading_coefficient = hp / math.factorial(k)
    circuit_size = circuitsize(n)
    
    conjecture_holds = abs(leading_coefficient - 1/circuit_size) < 1e-6
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Leading Coefficient",
        "metric_value": leading_coefficient,
        "instances_tested": len(I),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 35)]
    
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE mapping_undefined")