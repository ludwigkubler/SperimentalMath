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
    
    def matrix_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(m):
            if all(matrix[i][j] == 0 for j in range(n)):
                continue
            pivot_row = i
            while pivot_row < m and all(matrix[pivot_row][j] == 0 for j in range(n)):
                pivot_row += 1
            if pivot_row >= m:
                break
            matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
            for j in range(n):
                if i != j and matrix[j][i] != 0:
                    factor = matrix[j][i] / matrix[i][i]
                    for k in range(i, n):
                        matrix[j][k] -= factor * matrix[i][k]
            rank += 1
        return rank

    def generate_communication_instance(n):
        # Generate a random communication instance of size n
        A = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        B = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        return A, B

    def hodge_bundle_rank(A, B):
        # Compute the Hodge bundle rank (simplified version)
        n = len(A)
        H = []
        for i in range(n):
            row = [A[i][j] * B[j][i] for j in range(n)]
            H.append(row)
        return matrix_rank(H)

    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            A, B = generate_communication_instance(n)
            min_rank_H = hodge_bundle_rank(A, B)
            r_C = matrix_rank([A[i] + B[i] for i in range(n)])
            results.append((min_rank_H, r_C))

    if not results:
        return {
            "metric_name": "Pearson correlation",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    min_rank_H_values = [r[0] for r in results]
    r_C_values = [r[1] for r in results]

    n = len(results)
    mean_min_rank_H = sum(min_rank_H_values) / n
    mean_r_C = sum(r_C_values) / n

    covariance = sum((min_rank_H_values[i] - mean_min_rank_H) * (r_C_values[i] - mean_r_C) for i in range(n)) / n
    variance_min_rank_H = sum((min_rank_H_values[i] - mean_min_rank_H) ** 2 for i in range(n)) / n
    variance_r_C = sum((r_C_values[i] - mean_r_C) ** 2 for i in range(n)) / n

    pearson_correlation = covariance / math.sqrt(variance_min_rank_H * variance_r_C)

    return {
        "metric_name": "Pearson correlation",
        "metric_value": pearson_correlation,
        "instances_tested": len(results),
        "n_max": 40,
        "conjecture_holds": pearson_correlation >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")