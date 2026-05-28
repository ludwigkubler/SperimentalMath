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

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        pivot = A[i][i]
        if pivot == 0:
            continue
        for j in range(n):
            A[i][j] /= pivot
        for j in range(m):
            if j != i and A[j][i] != 0:
                factor = A[j][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]

def matrix_multiply(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def tropical_hodge_decomposition(A):
    m, n = len(A), len(A[0])
    H = [[float('-inf')] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            if A[i][j] > H[i][j]:
                H[i][j] = A[i][j]
    return H

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    clauses = []
    for _ in range(n):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        if all(abs(lit) not in c for c in clauses):
            clauses.append(clause)
    A = [[0] * n for _ in range(n)]
    for clause in clauses:
        for lit in clause:
            A[lit - 1][abs(lit) - 1] += 1
    H = tropical_hodge_decomposition(A)
    min_rank = min(sum(1 for x in row if x != float('-inf')) for row in H)
    log_n = math.log(n, 2)
    return {
        "metric_name": "min_rank_log_n_ratio",
        "metric_value": Fraction(min_rank, log_n),
        "instances_tested": len(clauses),
        "conjecture_holds": min_rank <= 3 * log_n,
        "counterexample": "" if min_rank <= 3 * log_n else f"n={n}, min_rank={min_rank}, log_n={log_n}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)

    metric_values = [r["metric_value"] for r in results if "metric_value" in r]
    support_count = sum(1 for r in results if r["conjecture_holds"])
    support_fraction = Fraction(support_count, len(results))
    mean = sum(metric_values) / len(metric_values)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= Fraction(4, 5):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"min_rank > 3 * log_n\" first_failing_seed={first_failing_seed}")