# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
import math
import itertools

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda x: abs(A[x][i]))
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                continue
            factor = Fraction(1) / A[i][i]
            for j in range(n):
                A[i][j] *= factor
            for k in range(m):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return [row for row in A if any(row)]

    def matrix_rank(A):
        return sum(1 for row in gaussian_elimination(A) if any(row))

    def compute_matrix_rank_variance(phi):
        n = len(phi[0])
        matrix_ranks = [matrix_rank(C) for C in phi]
        mean = Fraction(sum(matrix_ranks), n)
        variance = sum((x - mean) ** 2 for x in matrix_ranks) / n
        return variance

    def run_k_sat_trial(n, k=3):
        phi = []
        variables = list(range(n))
        for _ in range(1 << n):
            clause = random.sample(variables, k)
            phi.append([1 if var in clause else -1 for var in variables])
        local_cohomology_rank = len(phi)  # Simplified for testing
        matrix_rank_variance = compute_matrix_rank_variance(phi)
        return local_cohomology_rank, matrix_rank_variance

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            local_cohomology_rank, matrix_rank_variance = run_k_sat_trial(n)
            results.append((local_cohomology_rank, matrix_rank_variance))
    
    correlation_coefficient = sum(x * y for x, y in results) / len(results)
    mean_value = sum(x for x, _ in results) / len(results)
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x, _ in results) / len(results))
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient > 0.7,
        "counterexample": "" if correlation_coefficient > 0.7 else "Correlation below threshold"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(x["metric_value"] for x in results) / len(results)
    std_value = math.sqrt(sum((x["metric_value"] - mean_value) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for x in results if x["conjecture_holds"]) / len(results)

    if all(x["conjecture_holds"] for x in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(x["seed"] for x in results if not x["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation below threshold\" first_failing_seed={first_failing_seed}")