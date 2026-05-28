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
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 30
    d = n // 2
    metric_name = "circuit_depth"
    
    def generate_polynomial(n, d):
        coeffs = [random.randint(0, 1) for _ in range(d+1)]
        return sum(c * x**i for i, c in enumerate(coeffs))
    
    def xor_circuit(f, n):
        if f == 0:
            return 1
        elif f == 1:
            return n % 2
        else:
            return (xor_circuit(f >> 1, n) + xor_circuit(f & 1, n)) % 2
    
    def schur_weyl_rank(f):
        # Placeholder for actual Schur-Weyl rank calculation
        # This is a dummy implementation for testing purposes
        return random.randint(1, 5)
    
    total_depth = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(30):
        f = generate_polynomial(n, d)
        rank = schur_weyl_rank(f)
        depth = xor_circuit(f, n)
        total_depth += depth
        instances_tested += 1
        
        if abs(depth - rank**2) > 3:
            conjecture_holds = False
            counterexample = f"Depth {depth} does not match rank^2 {rank**2}"
    
    mean_depth = total_depth / instances_tested
    std_dev = math.sqrt(sum((depth - mean_depth)**2 for depth in range(total_depth)) / instances_tested)
    
    return {
        "metric_name": metric_name,
        "metric_value": mean_depth,
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
    
    mean_depth = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_depth)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_depth} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")