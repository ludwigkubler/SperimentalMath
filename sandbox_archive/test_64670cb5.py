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
        n = len(A)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            if pivot == 0:
                continue
            for j in range(n):
                if j != i:
                    factor = A[j][i] / pivot
                    for k in range(n + 1):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiplication(A, B):
        n = len(A)
        C = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def determinant(A):
        n = len(A)
        if n == 1:
            return A[0][0]
        det = 0
        sign = 1
        for i in range(n):
            submatrix = [row[:i] + row[i+1:] for row in A[1:]]
            det += sign * A[0][i] * determinant(submatrix)
            sign *= -1
        return det

    def cohomology_order(A):
        n = len(A)
        if n == 1:
            return 1
        A_augmented = [row + [1] for row in A]
        rref = gaussian_elimination(A_augmented)
        free_vars = sum(1 for row in rref if any(x != 0 for x in row[:-1]))
        return n - free_vars

    def variance(data):
        mean = sum(data) / len(data)
        return sum((x - mean) ** 2 for x in data) / len(data)

    instances_tested = 0
    cohomology_ratio_sum = 0.0
    n_max = 1

    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        for _ in range(5):
            instance = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
            cohomology_order_value = cohomology_order(instance)
            variance_value = variance([sum(row) for row in instance])
            if variance_value == 0:
                continue
            cohomology_ratio = cohomology_order_value / variance_value
            cohomology_ratio_sum += cohomology_ratio
            instances_tested += 1

    mean_cohomology_ratio = cohomology_ratio_sum / instances_tested
    conjecture_holds = mean_cohomology_ratio <= 10.0  # Arbitrary constant for testing
    counterexample = "Ratio exceeds bound" if not conjecture_holds else ""

    return {
        "metric_name": "cohomology_ratio",
        "metric_value": mean_cohomology_ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='Ratio exceeds bound' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")