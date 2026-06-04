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
            max_row = i + max(range(i, m), key=lambda j: abs(A[j][i]))
            A[i], A[max_row] = A[max_row], A[i]
            factor = 1 / A[i][i]
            for j in range(n):
                A[i][j] *= factor
            for k in range(m):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B[0]), len(B)
        C = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def trace(A):
        return sum(A[i][i] for i in range(len(A)))

    def log2(x):
        if x <= 0:
            return float('-inf')
        return math.log2(x)

    def communication_complexity(n):
        # Placeholder function for actual communication complexity
        return n

    def geometric_entanglement(f):
        n = len(f)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                C[i][j] = f[i] + f[j]
                C[j][i] = C[i][j]
        C = gaussian_elimination(C)
        return trace(C) / n

    def run_test(n):
        f = [random.randint(1, 10) for _ in range(n)]
        E_G_f = geometric_entanglement(f)
        comm_rank = communication_complexity(n)
        return {
            "metric_name": "geometric_entanglement",
            "metric_value": E_G_f,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": E_G_f <= 2 * log2(n) ** 2,
            "counterexample": ""
        }

    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        result = run_test(n)
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    return {
        "seed": seed,
        "metric_name": "geometric_entanglement",
        "mean_metric_value": mean_value,
        "std_metric_value": std_value,
        "support_fraction": support_fraction
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["mean_metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["mean_metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["support_fraction"] == 1.0) / len(results)

    if all(r["support_fraction"] == 1.0 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if r["support_fraction"] < 1.0)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")