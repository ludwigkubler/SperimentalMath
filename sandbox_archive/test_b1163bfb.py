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
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0 for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][k] += A[i][j] * B[j][k]
        return C

    def local_coherence_rank(A):
        m, n = len(A), len(A[0])
        I = [[1 if i == j else 0 for j in range(n)] for i in range(m)]
        augmented_matrix = [A[i] + I[i] for i in range(m)]
        reduced_matrix = gaussian_elimination(augmented_matrix)
        rank = sum(1 for row in reduced_matrix if any(row))
        return rank

    def communication_complexity(protocol):
        # Placeholder function to compute communication complexity
        # This is a dummy implementation and should be replaced with actual logic
        return len(protocol)

    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_metric_value = 0.0
    max_n = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):
            protocol = [random.randint(1, n) for _ in range(n)]
            C_P = communication_complexity(protocol)
            mlcr_P = local_coherence_rank(matrix_multiply([[i] * n for i in range(n)], [[j] * n for j in range(n)]))
            instances_tested += 1
            max_n = max(max_n, n)
            k_values = [0.5, 1.0, 1.5]
            for k in k_values:
                diff = abs(mlcr_P - k * C_P)
                if diff > 0.1:  # Threshold value
                    conjecture_holds = False
                    counterexample = f"n={n}, mlcr(P)={mlcr_P}, C(P)={C_P}, k={k}, diff={diff}"
                    break

    return {
        "metric_name": "mlcr_diff",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unreachable")