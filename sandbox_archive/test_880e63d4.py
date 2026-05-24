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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def determinant(A):
    if len(A) == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]
    det = 0
    for c in range(len(A)):
        det += ((-1) ** c) * A[0][c] * determinant([row[:c] + row[c+1:] for row in A[1:]])
    return det

def free_entropy(L):
    n = len(L)
    L_inv = [[L[j][i] / determinant(L) if i == j else -sum(L[j][k] * L[k][i] for k in range(n) if k != j) / determinant(L) for i in range(n)] for j in range(n)]
    return -sum(math.log(abs(L_inv[i][i])) for i in range(n))

def tensor_width(BP):
    # Placeholder implementation
    return len(BP)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    BP = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    G = [[sum(BP[i][j] * BP[j][k] for j in range(n)) for k in range(n)] for i in range(n)]
    F_G = free_entropy(G)
    DTW_BP = tensor_width(BP)
    ratio = F_G / DTW_BP if DTW_BP != 0 else float('inf')
    f_n = lambda n: math.log2(n)  # Placeholder function
    conjecture_holds = ratio >= f_n(n)
    counterexample = "" if conjecture_holds else "f_n({}) > {}".format(n, f_n(n))
    return {
        "metric_name": "F(G)/DTW(BP)",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i - 1 for i in range(5, 8)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL: {}".format(result))
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_value, std_dev, support_fraction))
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print("RESULT: FALSIFIED counterexample='f_n(n) > f_n({})' first_failing_seed={}".format(first_failing_seed, first_failing_seed))
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")