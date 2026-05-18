# auto-injected by SEC sandbox
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import itertools
from fractions import Fraction

def matrix_mult(a, b):
    """Multiply two matrices a and b."""
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]

def matrix_add(a, b):
    """Add two matrices a and b."""
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]

def matrix_scalar_mult(a, scalar):
    """Multiply matrix a by a scalar."""
    return [[a[i][j] * scalar for j in range(len(a[0]))] for i in range(len(a))]

def matrix_to_vector(m):
    """Convert a matrix to a vector by concatenating rows."""
    return [m[i][j] for i in range(len(m)) for j in range(len(m[0]))]

def vector_to_matrix(v, rows, cols):
    """Convert a vector to a matrix with given rows and columns."""
    return [[v[i * cols + j] for j in range(cols)] for i in range(rows)]

def gaussian_elimination(matrix):
    """Perform Gaussian elimination on a matrix."""
    rows = len(matrix)
    cols = len(matrix[0]) if rows > 0 else 0
    rank = 0
    for col in range(cols):
        pivot = rank
        while pivot < rows and matrix[pivot][col] == 0:
            pivot += 1
        if pivot == rows:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        pivot_val = matrix[rank][col]
        for c in range(col, cols):
            matrix[rank][c] = Fraction(matrix[rank][c], pivot_val)
        for r in range(rows):
            if r != rank and matrix[r][col] != 0:
                factor = matrix[r][col]
                for c in range(col, cols):
                    matrix[r][c] -= factor * matrix[rank][c]
        rank += 1
    return rank

def compute_span_closure(matrices, w):
    """Compute the span closure of a set of matrices."""
    basis = [matrix_to_vector(m) for m in matrices]
    basis.append(matrix_to_vector([[1 if i == j else 0 for j in range(w)] for i in range(w)]))  # Add identity matrix
    new_basis = basis.copy()
    while True:
        temp_basis = new_basis.copy()
        for a, b in itertools.product(new_basis, repeat=2):
            product = matrix_mult(vector_to_matrix(a, w, w), vector_to_matrix(b, w, w))
            product_vec = matrix_to_vector(product)
            if product_vec not in temp_basis:
                temp_basis.append(product_vec)
        if len(temp_basis) == len(new_basis):
            break
        new_basis = temp_basis
    matrix_basis = [vector_to_matrix(v, w, w) for v in new_basis]
    augmented_matrix = [matrix_to_vector(m) for m in matrix_basis]
    rank = gaussian_elimination(augmented_matrix)
    return rank

def generate_random_bp(n, w, seed):
    """Generate a random read-twice oblivious BP."""
    random.seed(seed)
    L = 4 * n
    var_positions = {i: random.sample(range(L), 2) for i in range(2 * n)}
    T = []
    for _ in range(L):
        T_layer = []
        for _ in range(w):
            row = [0] * w
            non_zero_pos = random.randint(0, w - 1)
            row[non_zero_pos] = 1
            T_layer.append(row)
        T.append(T_layer)
    return var_positions, T

def compute_rho(P, w):
    """Compute ρ(P) for a given BP P."""
    var_positions, T = P
    matrices = []
    for i in range(len(T)):
        matrices.append(T[i])
    for i in range(len(T)):
        for j in range(i + 1, len(T)):
            product = matrix_mult(T[i], T[j])
            matrices.append(product)
    rank = compute_span_closure(matrices, w)
    return math.log2(rank + 1)

def run_trial(seed):
    """Run a single trial with the given seed."""
    random.seed(seed)
    n = random.choice([3, 4, 5, 6, 7, 8])
    w = random.choice([4, 8])
    P = generate_random_bp(n, w, seed)
    rho = compute_rho(P, w)
    conjecture_holds = rho <= 2 * math.log2(w + 1)
    counterexample = "" if conjecture_holds else f"rho={rho} > 2*log2(w+1)={2*math.log2(w+1)}"
    return {
        "metric_name": "rho",
        "metric_value": rho,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    metric_values = [r["metric_value"] for r in results]
    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")