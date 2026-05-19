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
    n = 40  # Maximum size for this problem
    p = math.log(n)

    def generate_disjointness_matrix(n):
        M = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                M[i][j] = random.randint(1, 2)
                M[j][i] = 3 - M[i][j]
        return M

    def svd(M):
        # Simple SVD implementation using power iteration method
        u = [random.random() for _ in range(n)]
        v = [random.random() for _ in range(n)]
        sigma = [1.0] * n
        tol = 1e-6
        max_iter = 1000

        def matmul(A, B):
            return [[sum(a * b for a, b in zip(row_a, col_b)) for col_b in zip(*B)] for row_a in A]

        def transpose(M):
            return [list(col) for col in zip(*M)]

        for _ in range(max_iter):
            u_new = matmul(M, v)
            sigma_new = [max(abs(u_new[i][j]) for j in range(n)) for i in range(n)]
            v_new = matmul(transpose(M), u_new)

            if max(abs(u_new[i] - u[i]) for i in range(n)) < tol and max(abs(v_new[j] - v[j]) for j in range(n)) < tol:
                break

            u, v = u_new, v_new
            sigma = sigma_new

        return u, sigma, transpose(v)

    M = generate_disjointness_matrix(n)
    U, S, Vt = svd(M)
    norm_p = sum(S[i] ** p for i in range(n)) ** (1 / p)

    metric_value = norm_p / n
    conjecture_holds = metric_value >= 0.1
    counterexample = "" if conjecture_holds else "Noncommutative L^p norm too small"

    return {
        "metric_name": "noncommutative_Lp_norm",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys

    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 3 for i in range(5, 8)]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Noncommutative L^p norm too small\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")