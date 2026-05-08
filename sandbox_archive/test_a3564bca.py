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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a*b) // gcd(a, b)

def matrix_multiply(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    augmented = [A[i] + [b[i]] for i in range(m)]
    for i in range(n):
        max_row = i
        for j in range(i+1, m):
            if abs(augmented[j][i]) > abs(augmented[max_row][i]):
                max_row = j
        augmented[i], augmented[max_row] = augmented[max_row], augmented[i]
        pivot = augmented[i][i]
        for j in range(n + 1):
            augmented[i][j] /= pivot
        for j in range(m):
            if j != i:
                factor = augmented[j][i]
                for k in range(n + 1):
                    augmented[j][k] -= factor * augmented[i][k]
    return [row[-1] for row in augmented]

def determinant(A):
    n = len(A)
    if n == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]
    det = 0
    sign = 1
    for i in range(n):
        submatrix = [row[:i] + row[i+1:] for row in A[1:]]
        det += sign * A[0][i] * determinant(submatrix)
        sign *= -1
    return det

def hilbert_series(poly, n):
    m = len(poly)
    h = [Fraction(1)] + [Fraction(0)] * (m-1)
    new_h = [Fraction(0)] * (m+n-1)
    for i in range(m):
        for j in range(n-i+1):
            new_h[j+i-1] += h[j] * poly[i]
    return new_h

def permanent(matrix):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    det = 0
    sign = 1
    for i in range(n):
        submatrix = [row[:i] + row[i+1:] for row in matrix[1:]]
        det += sign * matrix[0][i] * permanent(submatrix)
        sign *= -1
    return det

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = random.randint(1, math.isqrt(n**1.5))
        perm_n = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
        det_m = [[random.randint(-10, 10) for _ in range(m)] for _ in range(m)]
        
        perm_series = hilbert_series(permanent(perm_n), n)
        det_series = hilbert_series(determinant(det_m), m)
        
        perm_degree = len([x for x in perm_series if x != Fraction(0)]) - 1
        det_degree = len([x for x in det_series if x != Fraction(0)]) - 1
        
        results.append({
            "metric_name": "Hilbert Series Degree",
            "metric_value": perm_degree,
            "instances_tested": 1,
            "conjecture_holds": perm_degree > det_degree,
            "counterexample": "" if perm_degree > det_degree else f"perm_n={perm_n}, det_m={det_m}"
        })
    
    return {
        "metric_name": "Hilbert Series Degree",
        "metric_value": sum(result["metric_value"] for result in results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": all(result["conjecture_holds"] for result in results),
        "counterexample": next((result["counterexample"] for result in results if not result["conjecture_holds"]), "")
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3**j for i in range(5) for j in range(5)]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")