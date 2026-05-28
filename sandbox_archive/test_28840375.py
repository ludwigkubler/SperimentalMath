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

def matrix_multiplication(A, B):
    m = len(A)
    p = len(B[0])
    q = len(B)
    C = [[0 for _ in range(p)] for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(q):
                C[i][j] += A[i][k] * B[k][j]
    return C

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det += ((-1) ** j) * A[0][j] * determinant(submatrix)
    return det

def orthonormal_basis(matrix):
    n = len(matrix)
    basis = []
    for i in range(n):
        v = matrix[i]
        norm = math.sqrt(sum(x**2 for x in v))
        if norm == 0:
            continue
        v = [x / norm for x in v]
        basis.append(v)
        for j in range(i+1, n):
            u = matrix[j]
            dot_product = sum(a*b for a, b in zip(v, u))
            for k in range(n):
                matrix[j][k] -= dot_product * v[k]
    return basis

def geometric_phase_rank(matrix):
    basis = orthonormal_basis(matrix)
    rank = len(basis)
    return rank

def communication_complexity(n, t):
    min_r = float('inf')
    for r in range(1, n+1):
        value = math.factorial(r) * math.log(1/r) / math.log(t)
        if value < min_r:
            min_r = value
    return 2 ** (n/4 * min_r)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    t = random.uniform(1, 100)
    
    # Generate a random n-bit Boolean function
    support_manifold = [[random.choice([0, 1]) for _ in range(n)] for _ in range(2**n)]
    
    # Compute the geometric phase rank of the support manifold
    geometric_rank = geometric_phase_rank(support_manifold)
    
    # Calculate communication complexity for XORing two n-bit inputs
    cc_xor = communication_complexity(n, t)
    
    # Check if the conjecture holds
    conjecture_holds = geometric_rank <= cc_xor
    
    return {
        "metric_name": "geometric_phase_rank",
        "metric_value": geometric_rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Geometric phase rank {geometric_rank} > CC(XOR) {cc_xor}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results]
    conjecture_holds = all(r["conjecture_holds"] for r in results)
    
    if conjecture_holds:
        mean = sum(metric_values) / len(metric_values)
        std = math.sqrt(sum((x - mean)**2 for x in metric_values) / len(metric_values))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Geometric phase rank > CC(XOR)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")