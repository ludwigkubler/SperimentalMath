# auto-injected by SEC sandbox
import itertools
import collections
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import json
from fractions import Fraction

def matrix_mult(a, b):
    """Multiply two matrices a and b."""
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]

def matrix_add(a, b):
    """Add two matrices a and b."""
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]

def matrix_to_vector(m):
    """Convert a matrix to a vector by flattening it."""
    return [m[i][j] for i in range(len(m)) for j in range(len(m[0]))]

def vector_to_matrix(v, w):
    """Convert a vector to a matrix of size w x w."""
    return [[v[i * w + j] for j in range(w)] for i in range(w)]

def gaussian_elimination(matrix):
    """Perform Gaussian elimination on a matrix."""
    n = len(matrix)
    for i in range(n):
        # Find the row with the maximum element in the current column
        max_row = i
        for k in range(i + 1, n):
            if abs(matrix[k][i]) > abs(matrix[max_row][i]):
                max_row = k
        # Swap the current row with the max_row
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        # If the leading element is zero, the matrix is singular
        if matrix[i][i] == 0:
            continue
        # Normalize the current row
        for k in range(i + 1, n):
            factor = Fraction(matrix[k][i], matrix[i][i])
            for j in range(i, n):
                matrix[k][j] -= factor * matrix[i][j]
    return matrix

def compute_dimension(basis):
    """Compute the dimension of the space spanned by the basis vectors."""
    if not basis:
        return 0
    # Perform Gaussian elimination on the basis vectors
    basis = gaussian_elimination(basis)
    # Count the number of non-zero rows
    dimension = 0
    for row in basis:
        if any(row):
            dimension += 1
    return dimension

def generate_random_bp(n, w, seed):
    """Generate a random read-twice oblivious BP."""
    random.seed(seed)
    L = 4 * n
    # Assign each variable to exactly two random layer positions
    var_positions = {}
    for k in range(n):
        positions = random.sample(range(L), 2)
        var_positions[k] = positions
    # Generate random transition matrices
    T = []
    for i in range(L):
        T_i = []
        for b in [0, 1]:
            # Each row of T_i^{(b)} has at most one 1
            T_ib = [[0] * w for _ in range(w)]
            for j in range(w):
                if random.random() < 0.5:
                    k = random.randint(0, w - 1)
                    T_ib[j][k] = 1
            T_i.append(T_ib)
        T.append(T_i)
    return T, var_positions

def compute_rho(P, var_positions, w):
    """Compute ρ(P) for a given BP P."""
    # Initialize the basis with the identity matrix
    basis = [matrix_to_vector([[1 if i == j else 0 for j in range(w)] for i in range(w)])]
    # Generate all possible products of transition matrices
    for k in range(len(var_positions)):
        positions = var_positions[k]
        for b in [0, 1]:
            # Multiply the transition matrix T_i^{(b)} with the current basis
            new_basis = []
            for v in basis:
                m = vector_to_matrix(v, w)
                T_ib = P[positions[0]][b] if b == 0 else P[positions[1]][b]
                m_new = matrix_mult(m, T_ib)
                new_basis.append(matrix_to_vector(m_new))
            # Add the new basis vectors to the basis
            basis.extend(new_basis)
    # Compute the dimension of the space spanned by the basis vectors
    dimension = compute_dimension(basis)
    # Compute ρ(P)
    rho = math.log2(dimension + 1)
    return rho

def run_trial(seed):
    """Run a single trial with the given seed."""
    random.seed(seed)
    n = random.choice([3, 4, 5, 6, 7, 8])
    w = random.choice([4, 8])
    # Generate a random read-twice oblivious BP
    P, var_positions = generate_random_bp(n, w, seed)
    # Compute ρ(P)
    rho = compute_rho(P, var_positions, w)
    # Check the conjecture
    conjecture_holds = rho <= 2 * math.log2(w + 1)
    counterexample = "" if conjecture_holds else f"rho={rho} > 2*log2(w+1)={2*math.log2(w+1)}"
    return {
        "metric_name": "rho",
        "metric_value": rho,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def main():
    """Main function to run the trials."""
    seeds = sys.argv[1:] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps({'seed': seed, **result})}")
        results.append(result)
    # Compute statistics
    metric_values = [r["metric_value"] for r in results]
    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    # Determine the result
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample={r['counterexample']} first_failing_seed={seeds[results.index(r)]}")
                break

if __name__ == "__main__":
    main()