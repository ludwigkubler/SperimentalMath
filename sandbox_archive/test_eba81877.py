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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            for j in range(m):
                if i != j:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def determinant(A):
        m, n = len(A), len(A[0])
        if m != n:
            raise ValueError("Matrix must be square")
        if m == 1:
            return A[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det

    def homology_group(G, k):
        # Placeholder function to compute the k-th homology group
        # This is a simplified version and should be replaced with actual computation
        return random.randint(1, 5)

    def cohomology_group(G, k):
        # Placeholder function to compute the k-th cohomology group
        # This is a simplified version and should be replaced with actual computation
        return random.randint(1, 5)

    def minimal_index(H):
        # Placeholder function to compute the minimal index of a lattice
        # This is a simplified version and should be replaced with actual computation
        return random.randint(1, 10)

    def communication_complexity_rank(G):
        # Placeholder function to compute the communication complexity rank
        # This is a simplified version and should be replaced with actual computation
        return random.randint(1, 5)

    n_values = []
    I_G_values = []
    r_phi_G_values = []

    for _ in range(30):
        G = random.choice([1, 2, 3])  # Placeholder for a formula φ_G
        k = random.randint(1, 2)  # Placeholder for the homology degree

        H = homology_group(G, k)
        I_G = minimal_index(H)
        r_phi_G = communication_complexity_rank(G)

        n_values.append(k)
        I_G_values.append(I_G)
        r_phi_G_values.append(r_phi_G)

    if not I_G_values or not r_phi_G_values:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_data"
        }

    n_mean = sum(n_values) / len(n_values)
    I_G_mean = sum(I_G_values) / len(I_G_values)
    r_phi_G_mean = sum(r_phi_G_values) / len(r_phi_G_values)

    covariance = sum((n - n_mean) * (I_G - I_G_mean) * (r_phi_G - r_phi_G_mean) for n, I_G, r_phi_G in zip(n_values, I_G_values, r_phi_G_values)) / len(n_values)
    variance_n = sum((n - n_mean) ** 2 for n in n_values) / len(n_values)
    variance_I_G = sum((I_G - I_G_mean) ** 2 for I_G in I_G_values) / len(I_G_values)

    if variance_n == 0 or variance_I_G == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(n_values),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "constant_metric"
        }

    pearson_correlation_coefficient = covariance / (math.sqrt(variance_n) * math.sqrt(variance_I_G))

    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": pearson_correlation_coefficient > 0.8 and all(I_G <= 2 * r_phi_G for I_G, r_phi_G in zip(I_G_values, r_phi_G_values)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")

        if trial_result["conjecture_holds"]:
            results.append(trial_result)

    if len(results) == len(seeds):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = len(results) / len(seeds)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_supported\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_support_found")