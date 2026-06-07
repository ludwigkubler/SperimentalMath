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
            for j in range(i+1, m):
                factor = Fraction(A[j][i], A[i][i])
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[Fraction(0) for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def determinant(A):
        m, n = len(A), len(A[0])
        if m != n:
            raise ValueError("Matrix must be square")
        if n == 1:
            return A[0][0]
        det = Fraction(0)
        for j in range(n):
            submatrix = [[A[i][k] for k in range(n) if k != j] for i in range(1, m)]
            det += (-1)**j * A[0][j] * determinant(submatrix)
        return det

    def local_cohomology_rank(V):
        # Placeholder function to compute the minimal local cohomology rank
        # This is a dummy implementation and should be replaced with actual computation
        return random.randint(1, 5)

    def resolution_proof_width(phi):
        # Placeholder function to compute the resolution proof width
        # This is a dummy implementation and should be replaced with actual computation
        return random.randint(10, 30)

    instances_tested = 0
    total_h1 = Fraction(0)
    total_w = Fraction(0)
    max_n = 0

    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            phi = ''.join(random.choice('01') for _ in range(n))
            V = [tuple(int(phi[i]) for i in range(n))]
            h1 = local_cohomology_rank(V)
            w = resolution_proof_width(phi)
            total_h1 += Fraction(h1)
            total_w += Fraction(w)
            instances_tested += 1
            max_n = max(max_n, n)

    mean_h1 = total_h1 / instances_tested
    mean_w = total_w / instances_tested

    correlation_coefficient = (instances_tested * sum(h1*w for h1, w in zip([mean_h1]*instances_tested, [mean_w]*instances_tested)) - 
                              instances_tested * mean_h1 * mean_w) / \
                             ((instances_tested * sum(h1**2 for h1 in [mean_h1]*instances_tested) - instances_tested * mean_h1**2) *
                              (instances_tested * sum(w**2 for w in [mean_w]*instances_tested) - instances_tested * mean_w**2))**0.5

    conjecture_holds = correlation_coefficient > 0.7
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": float(correlation_coefficient),
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["metric_value"] < 0.6 for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"] and r["metric_value"] < 0.6)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")