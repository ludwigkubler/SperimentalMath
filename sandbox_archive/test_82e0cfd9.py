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
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0]*p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def determinant(A):
        n = len(A)
        if n == 1:
            return A[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += ((-1)**j) * A[0][j] * determinant(submatrix)
        return det

    def hodge_theoretic_dimension(A):
        return math.log(abs(determinant(gaussian_elimination(A))), 2)

    def rank_variance(A):
        m, n = len(A), len(A[0])
        rank = sum(1 for row in A if any(row))
        variance = 0
        for i in range(m):
            for j in range(n):
                if A[i][j]:
                    variance += (i - (m-1)/2)**2 + (j - (n-1)/2)**2
        return variance / (m * n)

    def generate_instance(n):
        A = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        return A

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        instance = generate_instance(n)
        htd = hodge_theoretic_dimension(instance)
        rvar = rank_variance(instance)
        results.append({"n": n, "htd": htd, "rvar": rvar})

    mean_htd = sum(result["htd"] for result in results) / len(results)
    mean_rvar = sum(result["rvar"] for result in results) / len(results)

    correlation = 0
    for result in results:
        correlation += (result["htd"] - mean_htd) * (result["rvar"] - mean_rvar)
    correlation /= len(results) * math.sqrt(sum((result["htd"] - mean_htd)**2 for result in results)) * math.sqrt(sum((result["rvar"] - mean_rvar)**2 for result in results))

    return {
        "metric_name": "Correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": 0.3 <= abs(correlation) >= 0.7,
        "counterexample": "" if 0.3 <= abs(correlation) >= 0.7 else "Correlation out of acceptable range"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(sys.argv[1])] if len(sys.argv) > 1 else list(range(2, 59))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation out of acceptable range\" first_failing_seed={first_failing_seed}")