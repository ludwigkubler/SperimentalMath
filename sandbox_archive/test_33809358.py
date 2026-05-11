# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import itertools

def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def matrix_add(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            C[i][j] = A[i][j] + B[i][j]
    return C

def is_rank_1(matrix):
    n = len(matrix)
    rank = 0
    seen = set()
    for i in range(n):
        if any(matrix[i][j] != 0 for j in range(n)):
            row = tuple(matrix[i])
            if row not in seen:
                seen.add(row)
                rank += 1
    return rank == 1

def generate_disjointness_instance(n):
    A = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    B = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    M = matrix_multiply(A, B)
    return M

def noncommutative_rank(M):
    n = len(M)
    bound = 2 ** (n // 2) / n
    max_k = int(bound) + 10
    for k in range(1, max_k):
        for A_combination in itertools.product([[0, 1], [1, 0]], repeat=k):
            for B_combination in itertools.product([[0, 1], [1, 0]], repeat=k):
                A = [[A_combination[i][j] for j in range(k)] for i in range(k)]
                B = [[B_combination[i][j] for j in range(k)] for i in range(k)]
                if matrix_multiply(A, B) == M:
                    return k
    return max_k

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 10
    M = generate_disjointness_instance(n)
    rank_noncommutative = noncommutative_rank(M)
    bound = 2 ** (n // 2) / n
    conjecture_holds = rank_noncommutative <= bound
    counterexample = "" if conjecture_holds else f"rank_noncommutative={rank_noncommutative}, bound={bound}"
    return {
        "metric_name": "noncommutative_rank",
        "metric_value": rank_noncommutative,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 8)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, {result}}}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")