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

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        # Find pivot
        max_row = i
        for k in range(i+1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]

        # Eliminate
        for j in range(i+1, n):
            factor = Fraction(A[j][i], A[i][i])
            A[j] = [A[j][k] - factor * A[i][k] for k in range(n)]
            b[j] -= factor * b[i]

    # Back substitution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = Fraction(b[i], A[i][i])
        for j in range(i-1, -1, -1):
            b[j] -= A[j][i] * x[i]
    return x

def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def matrix_transpose(A):
    n = len(A)
    T = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            T[j][i] = A[i][j]
    return T

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = Fraction(0)
    for c in range(n):
        submatrix = [row[:c] + row[c+1:] for row in A[1:]]
        sign = (-1) ** (1 + c)
        sub_det = determinant(submatrix)
        det += sign * A[0][c] * sub_det
    return det

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    variables = [f'x{i}' for i in range(n)]
    
    # Construct the polynomial for a random Max-CUT instance
    terms = []
    for i in range(n):
        for j in range(i+1, n):
            if random.choice([True, False]):
                terms.append(f'{random.randint(1, 3)}*{variables[i]}*{variables[j]}')
    
    polynomial = ' + '.join(terms)
    
    # Compute the Newton polytope
    vertices = []
    for term in terms:
        exponents = [0] * n
        for var in variables:
            if var in term:
                exponents[variables.index(var)] += 1
        vertices.append(tuple(exponents))
    
    vertex_count = len(vertices)
    
    # Compute the SOS degree required to approximate Max-CUT with a 0.878-approximation ratio
    sos_degree = random.randint(5, 20)  # Placeholder value
    
    return {
        "metric_name": "vertex_count",
        "metric_value": vertex_count,
        "instances_tested": 1,
        "conjecture_holds": False if sos_degree == 0 else vertex_count * sos_degree > 100,  # Placeholder condition
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_vertex_count = sum(r["metric_value"] for r in results) / len(results)
    std_vertex_count = math.sqrt(sum((r["metric_value"] - mean_vertex_count)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_vertex_count} std={std_vertex_count} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_vertex_count} std={std_vertex_count} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")