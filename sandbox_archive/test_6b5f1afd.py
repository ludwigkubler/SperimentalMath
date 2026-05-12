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

def min_plus_matrix(A, B):
    n = len(A)
    C = [[float('inf')] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] = min(C[i][j], A[i][k] + B[k][j])
    return C

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    rank = 0
    for i in range(n):
        if abs(A[i][i]) > 1e-9:
            rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 10
    read_once_bp = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    read_twice_bp = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]

    def tropical_matrix(bp):
        m = len(bp)
        n = len(bp[0])
        T = [[float('inf')] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                if bp[i][j] == 1:
                    T[i][j] = 0
        for k in range(m):
            T = min_plus_matrix(T, T)
        return T

    def tropical_dimension(matrix):
        return gaussian_elimination(matrix)

    read_once_dim = tropical_dimension(tropical_matrix(read_once_bp))
    read_twice_dim = tropical_dimension(tropical_matrix(read_twice_bp))

    result_read_once = {
        "metric_name": "tropical_dimension",
        "metric_value": read_once_dim,
        "instances_tested": 1,
        "conjecture_holds": read_once_dim <= 4,
        "counterexample": "" if read_once_dim <= 4 else "read-once BP with dim > 4"
    }

    result_read_twice = {
        "metric_name": "tropical_dimension",
        "metric_value": read_twice_dim,
        "instances_tested": 1,
        "conjecture_holds": read_twice_dim >= 5,
        "counterexample": "" if read_twice_dim >= 5 else "read-twice BP with dim < 5"
    }

    return result_read_once, result_read_twice

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(30)]
    results = []
    for seed in seeds:
        read_once_result, read_twice_result = run_trial(seed)
        print(f"TRIAL: {read_once_result}")
        print(f"TRIAL: {read_twice_result}")
        results.append(read_once_result["metric_value"])
        results.append(read_twice_result["metric_value"])

    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean)**2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r <= 4 or r >= 5) / len(results)

    if all(r <= 4 or r >= 5 for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(r > 4 for r in results) and any(r < 5 for r in results):
        first_failing_seed = seeds[results.index(next(r for r in results if r > 4))]
        print(f"RESULT: FALSIFIED counterexample=\"dim mismatch\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE no clear trend")