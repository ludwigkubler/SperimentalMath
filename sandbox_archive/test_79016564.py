# auto-injected by SEC sandbox
import collections
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import itertools
import json

def matrix_multiply(A, B):
    """Multiply two matrices A (m×n) and B (n×p) to get a (m×p) matrix."""
    m = len(A)
    n = len(A[0]) if m > 0 else 0
    p = len(B[0]) if len(B) > 0 else 0
    result = [[0 for _ in range(p)] for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                result[i][j] += A[i][k] * B[k][j]
    return result

def transpose(matrix):
    """Transpose a matrix."""
    return [list(row) for row in zip(*matrix)]

def svd(matrix):
    """Compute the singular value decomposition of a matrix."""
    A = matrix
    m = len(A)
    n = len(A[0]) if m > 0 else 0
    U = [[0.0 for _ in range(m)] for _ in range(m)]
    V = [[0.0 for _ in range(n)] for _ in range(n)]
    s = [0.0] * min(m, n)

    # Compute A^T A
    ATA = matrix_multiply(transpose(A), A)

    # Compute eigenvalues and eigenvectors of A^T A
    # Using a simple power method for demonstration
    for i in range(min(m, n)):
        # Initialize a random vector
        v = [random.random() for _ in range(n)]
        for _ in range(100):
            # Multiply by A^T A
            Av = [sum(ATA[j][k] * v[k] for k in range(n)) for j in range(n)]
            # Normalize
            norm = math.sqrt(sum(x**2 for x in Av))
            if norm == 0:
                break
            v = [x / norm for x in Av]
        # Compute singular value
        s[i] = math.sqrt(sum(v[k] * ATA[k][k] for k in range(n)))
        # Compute singular vector
        for j in range(n):
            V[j][i] = v[j]

    # Compute U
    for i in range(m):
        for j in range(min(m, n)):
            if s[j] == 0:
                continue
            U[i][j] = sum(A[i][k] * V[k][j] for k in range(n)) / s[j]

    return U, s, V

def compute_spectral_excess(M, k, seed):
    """Compute the spectral excess ξ(M) for a given matrix M."""
    N = len(M)
    random.seed(seed)
    excess = 0.0
    instances_tested = 0

    for _ in range(30):
        # Select k random columns
        columns = random.sample(range(N), k)
        # Extract the submatrix
        submatrix = [[M[i][j] for j in columns] for i in range(N)]
        # Compute the SVD
        _, s, _ = svd(submatrix)
        # Compute the spectral norm squared
        spectral_norm_sq = s[0] ** 2
        # Add to the excess
        excess += (spectral_norm_sq / N) - 1
        instances_tested += 1

    return excess / 30, instances_tested

def construct_disj_matrix(n):
    """Construct the DISJ matrix for a given n."""
    N = 2 ** n
    M = [[0 for _ in range(N)] for _ in range(N)]
    for x in range(N):
        for y in range(N):
            # Check if x and y are disjoint
            if x & y == 0:
                M[x][y] = 1
    return M

def construct_parity_matrix(n):
    """Construct the PARITY matrix for a given n."""
    N = 2 ** n
    M = [[0 for _ in range(N)] for _ in range(N)]
    for x in range(N):
        for y in range(N):
            # Compute the parity of the bitwise AND of x and y
            parity = bin(x & y).count('1') % 2
            M[x][y] = 1 - parity
    return M

def construct_random_matrix(n):
    """Construct a random Boolean matrix for a given n."""
    N = 2 ** n
    M = [[0 for _ in range(N)] for _ in range(N)]
    for x in range(N):
        for y in range(N):
            M[x][y] = random.randint(0, 1)
    return M

def center_matrix(M):
    """Center the matrix M to M̃ = 2M − J."""
    N = len(M)
    J = [[1 for _ in range(N)] for _ in range(N)]
    M_tilde = [[2 * M[i][j] - J[i][j] for j in range(N)] for i in range(N)]
    return M_tilde

def run_trial(seed):
    """Run a single trial for a given seed."""
    random.seed(seed)
    n_values = [3, 4, 5]
    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        N = 2 ** n
        k = math.ceil(math.log2(N))

        # Construct and center the DISJ matrix
        M_disj = construct_disj_matrix(n)
        M_disj_tilde = center_matrix(M_disj)
        xi_disj, instances = compute_spectral_excess(M_disj_tilde, k, seed)
        instances_tested += instances

        # Construct and center the PARITY matrix
        M_parity = construct_parity_matrix(n)
        M_parity_tilde = center_matrix(M_parity)
        xi_parity, instances = compute_spectral_excess(M_parity_tilde, k, seed)
        instances_tested += instances

        # Construct and center a random matrix
        M_random = construct_random_matrix(n)
        M_random_tilde = center_matrix(M_random)
        xi_random, instances = compute_spectral_excess(M_random_tilde, k, seed)
        instances_tested += instances

        # Check the conjecture conditions
        if xi_disj < 0.5 * k / n or xi_parity > 0.05 or xi_random > 0.3 * k / N:
            conjecture_holds = False
            counterexample = f"n={n}, xi_disj={xi_disj}, xi_parity={xi_parity}, xi_random={xi_random}"

        metric_values.append(xi_disj)

    return {
        "metric_name": "spectral_excess",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        result["seed"] = seed
        print(f"TRIAL: {json.dumps(result)}")
        results.append(result)

    # Compute statistics
    metric_values = [r["metric_value"] for r in results]
    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    # Determine the final result
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")