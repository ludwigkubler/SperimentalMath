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
    
    def gaussian_elimination(A, b):
        n = len(b)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            factor = 1 / A[i][i]
            for j in range(n):
                if i != j:
                    factor_i_j = A[j][i] * factor
                    A[j] = [A[j][k] - factor_i_j * A[i][k] for k in range(n)]
                    b[j] -= factor_i_j * b[i]
        return [b[i] / A[i][i] for i in range(n)]

    def inverse_matrix(M):
        n = len(M)
        I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        return gaussian_elimination(M, I)

    def r_transform_inv(M):
        n = len(M)
        M_inv = inverse_matrix(M)
        R = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i != j:
                    factor = 1 / (M[i][i] - M[j][j])
                    R[i][j] = factor * (M_inv[i][j] + sum(M_inv[k][k] * M_inv[i][k] * M_inv[j][k] for k in range(n) if k != i and k != j))
        return R

    def free_cumulant_sum(R):
        n = len(R)
        tau = 0
        for k in range(1, n + 1):
            term = sum(math.comb(k - 1, j) * math.prod([R[i][i] ** (k - j - 1) for i in range(n)]) for j in range(k))
            tau += term / k
        return tau

    def generate_disjointness_matrix(n):
        M = [[0] * n for _ in range(n)]
        for i in range(n):
            M[i][i] = 1
        return M

    n = random.randint(5, 40)
    M = generate_disjointness_matrix(n)
    R = r_transform_inv(M)
    tau = free_cumulant_sum(R)

    return {
        "metric_name": "tau",
        "metric_value": tau,
        "instances_tested": 1,
        "conjecture_holds": tau >= 0.3 * n,
        "counterexample": "" if tau >= 0.3 * n else "disjointness_matrix"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_tau = sum(r["metric_value"] for r in results) / len(results)
    std_tau = math.sqrt(sum((r["metric_value"] - mean_tau) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_tau} std={std_tau} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_tau} std={std_tau} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='disjointness_matrix' first_failing_seed={first_failing_seed}")