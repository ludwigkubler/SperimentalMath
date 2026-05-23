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
    n = len(A)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
        A[i], A[max_row] = A[max_row], A[i]
        pivot = A[i][i]
        if pivot == 0:
            continue
        for j in range(n):
            A[i][j] /= pivot
        for k in range(n):
            if k != i:
                factor = A[k][i]
                for j in range(n):
                    A[k][j] -= factor * A[i][j]

def matrix_multiplication(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def hodge_rank(T):
    n = len(T)
    H = [[[float('inf')] * n for _ in range(n)] for _ in range(n)]
    for d in range(n):
        for i in range(n):
            for j in range(n):
                if T[i][j] == 1:
                    H[d][i][j] = 0
                else:
                    H[d][i][j] = float('inf')
    gaussian_elimination(H[0])
    rank = sum(all(row[j] == 0 for row in H[0]) for j in range(n))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    f = {i: random.choice([0, 1]) for i in range(n)}
    T = [[f[i] if j == i else 0 for j in range(n)] for i in range(n)]
    rank = hodge_rank(T)
    comm_complexity = n
    metric_value = rank
    instances_tested = 1
    conjecture_holds = rank >= n
    counterexample = "" if conjecture_holds else "f={}".format(f)
    return {
        "metric_name": "Hodge Rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL: {}".format(result))
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_metric_value, std_metric_value, support_fraction))
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        print("RESULT: FALSIFIED counterexample='{}' first_failing_seed={}".format(next(r["counterexample"] for r in results if not r["conjecture_holds"]), next(i for i, r in enumerate(results) if not r["conjecture_holds"])))
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")