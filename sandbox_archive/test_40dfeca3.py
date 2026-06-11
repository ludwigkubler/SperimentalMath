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
            max_row = i + random.randint(0, m - i - 1)
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            if pivot == 0:
                continue
            for j in range(n):
                A[i][j] /= pivot
            for k in range(m):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def rank_variance(A):
        m, n = len(A), len(A[0])
        U, S, Vt = gaussian_elimination([[A[i][j] for j in range(n)] for i in range(m)])
        rank = sum(1 for s in S if abs(s) > 1e-9)
        return (m - rank) * (n - rank)

    def mld(A):
        m, n = len(A), len(A[0])
        U, S, Vt = gaussian_elimination([[A[i][j] for j in range(n)] for i in range(m)])
        rank = sum(1 for s in S if abs(s) > 1e-9)
        return rank

    def check_conjecture(A, c):
        mld_val = mld(A)
        r_var = rank_variance(A)
        return mld_val <= c * r_var

    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_metric_value = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            A = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
            instances_tested += 1
            total_metric_value += rank_variance(A)
            if not check_conjecture(A, 1):
                conjecture_holds = False
                counterexample = f"Rank variance {rank_variance(A)} is greater than mld {mld(A)}"
                break

    mean_metric_value = total_metric_value / instances_tested
    support_fraction = int(conjecture_holds) * 100 / len(n_values)

    return {
        "metric_name": "mean_rank_variance",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(int(r["conjecture_holds"]) for r in results) * 100 / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")