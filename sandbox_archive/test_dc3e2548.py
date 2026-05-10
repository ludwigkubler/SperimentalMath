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
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(n):
                if j != i:
                    factor = A[j][i] / A[i][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def spectral_radius(matrix):
        n = len(matrix)
        eigenvalues = [1.0] * n
        for _ in range(100):  # Power iteration method
            v = [random.random() for _ in range(n)]
            v /= sum(v)
            Av = matrix_multiply(matrix, v)
            lambda_new = max(abs(x) for x in Av)
            if abs(lambda_new - eigenvalues[-1]) < 1e-6:
                break
            eigenvalues.append(lambda_new)
        return eigenvalues

    def free_entropy(eigenvalues):
        return -sum(math.log(abs(z)) for z in eigenvalues)

    n = random.randint(5, 40)
    seed += n  # Ensure different seeds for different sizes
    random.seed(seed)

    # Generate a read-twice branching program for IP_2
    transition_matrix = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        transition_matrix[i][i] = 1

    # Compute the spectral radius and free entropy
    eigenvalues = spectral_radius(transition_matrix)
    lambda_P = max(abs(z) for z in eigenvalues)
    phi_mu_P = free_entropy(eigenvalues)

    # Determine if the program is trivial or nontrivial
    is_trivial = all(x == 1 for x in transition_matrix[0])
    conjecture_holds = (is_trivial and phi_mu_P == math.log(n)) or (not is_trivial and phi_mu_P >= n)
    counterexample = "mapping_undefined" if not conjecture_holds else ""

    return {
        "metric_name": "Free Entropy Gap",
        "metric_value": phi_mu_P,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']:.6f}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")

    phi_mu_P_values = [r["metric_value"] for r in results]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(phi_mu_P_values)/len(phi_mu_P_values):.6f} std=0 support_fraction=1")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(phi_mu_P_values)/len(phi_mu_P_values):.6f} std={math.sqrt(sum((x - sum(phi_mu_P_values)/len(phi_mu_P_values))**2 for x in phi_mu_P_values) / len(phi_mu_P_values)):.6f} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")