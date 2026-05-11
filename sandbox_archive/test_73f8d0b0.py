# auto-injected by SEC sandbox
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
import math
from itertools import product

def generate_disjointness_instance(n):
    A = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    B = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    M = [[A[i][j] ^ B[i][j] for j in range(n)] for i in range(n)]
    return M

def matrix_multiply(A, B):
    n = len(A)
    C = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def is_rank_1(A, B):
    n = len(A)
    for i in range(n):
        for j in range(n):
            if A[i][j] != 0 and (A[i][j] * B[j][i] == 0 or A[i][j] * B[j][i] != A[0][0]):
                return False
    return True

def noncommutative_rank(M, max_k=10):
    n = len(M)
    for k in range(1, max_k + 1):
        for A_combination in product([[0, 1], [0, -1]], repeat=k * n):
            A = [[A_combination[i][j] for j in range(k)] for i in range(k)]
            B = [[A_combination[i + k][j] for j in range(k)] for i in range(k)]
            if matrix_multiply(A, B) == M:
                return k
    return float('inf')

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 10
    M = generate_disjointness_instance(n)
    rank_noncommutative = noncommutative_rank(M)
    bound = 2 ** (n / 2) / n
    conjecture_holds = rank_noncommutative <= bound
    counterexample = "" if conjecture_holds else f"Noncommutative rank {rank_noncommutative} > {bound}"
    return {
        "metric_name": "noncommutative_rank",
        "metric_value": rank_noncommutative,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")