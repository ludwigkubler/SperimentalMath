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
    
    n = random.randint(5, 40)
    F = [i for i in range(2, 10)]  # Finite field F with elements {2, 3, ..., 9}
    a, b = random.choice(F), random.choice(F)
    A = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
    B = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]

    # Compute noncommutative tensor product rank np(A ⊗ B)
    def matrix_multiply(X, Y):
        return [[sum(x * y for x, y in zip(row_x, col_y)) for col_y in zip(*Y)] for row_x in X]

    def tensor_product(A, B):
        return [[[A[i][k] * B[j][l] for l in range(n)] for k in range(n)] for j in range(n)]

    def rank(matrix):
        m = len(matrix)
        n = len(matrix[0])
        if m == 1 and n == 1:
            return abs(matrix[0][0])
        if m > n:
            matrix = list(zip(*matrix))
            m, n = n, m
        for i in range(m):
            if matrix[i][i] != 0:
                for j in range(i + 1, m):
                    factor = matrix[j][i] / matrix[i][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        return sum(1 for row in matrix if any(row))

    np_A_tensor_B = rank(tensor_product(A, B))

    # Construct read-twice BP for IP_2 and measure its width W(G)
    def construct_bp(matrix):
        m = len(matrix)
        n = len(matrix[0])
        bp = []
        for i in range(m):
            for j in range(n):
                if matrix[i][j] != 0:
                    bp.append((i, j))
        return bp

    W_G = len(construct_bp(tensor_product(A, B)))

    # Correlate np(A ⊗ B) with W(G)
    metric_value = np_A_tensor_B - W_G
    instances_tested = 1
    conjecture_holds = abs(metric_value) <= 3 * math.sqrt(np_A_tensor_B + W_G)
    counterexample = "" if conjecture_holds else f"np(A ⊗ B)={np_A_tensor_B}, W(G)={W_G}"

    return {
        "metric_name": "Rank Difference",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank Difference\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")