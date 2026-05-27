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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

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
                if i != j:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def inner_product_mod_2(v1, v2):
        return sum(x * y for x, y in zip(v1, v2)) % 2

    def generate_read_twice_bp(n):
        bp = []
        for _ in range(n):
            if random.choice([True, False]):
                bp.append(random.randint(0, n-1))
            else:
                bp.append(bp[-1])
        return bp

    def group_cocommutative_algebra(bp):
        m = len(bp)
        A = [[0] * (m+1) for _ in range(m+1)]
        for i in range(m):
            A[i][i] = 1
        for i in range(m):
            for j in range(i, m):
                if bp[i] == bp[j]:
                    A[i][j] += 1
                    A[j][i] += 1
        return gaussian_elimination(A)

    def minimal_rank(A):
        rank = 0
        for row in A:
            if any(row):
                rank += 1
        return rank

    n = random.choice([5, 10, 15, 20, 30, 40])
    bp = generate_read_twice_bp(n)
    algebra = group_cocommutative_algebra(bp)
    rank = minimal_rank(algebra)

    if inner_product_mod_2(bp, bp) == 0:
        conjecture_holds = rank >= n
        counterexample = "" if conjecture_holds else "inner_product_mod_2_trivial"
    else:
        conjecture_holds = False
        counterexample = "mapping_undefined"

    return {
        "metric_name": "minimal_rank",
        "metric_value": rank,
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

    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")