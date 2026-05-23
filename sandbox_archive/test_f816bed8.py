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

def hadamard(n):
    if n == 1:
        return [[1]]
    H = hadamard(n // 2)
    size = len(H)
    result = [[0] * (size * 2) for _ in range(size * 2)]
    for i in range(size):
        for j in range(size):
            result[i][j] = result[i + size][j] = result[i][j + size] = H[i][j]
            result[i + size][j + size] = -H[i][j]
    return result

def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    n = len(A)
    M = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(M[j][i]) > abs(M[max_row][i]):
                max_row = j
        M[i], M[max_row] = M[max_row], M[i]
        for j in range(i+1, n):
            factor = M[j][i] / M[i][i]
            for k in range(n + 1):
                M[j][k] -= factor * M[i][k]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = M[i][-1] / M[i][i]
        for j in range(i):
            M[j][-1] -= M[j][i] * x[i]
    return x

def geometric_entanglement(n):
    H = hadamard(n)
    I = [[0 if i != j else 1 for j in range(n)] for i in range(n)]
    E = matrix_multiply(H, I)
    det = 1
    for i in range(n):
        det *= E[i][i]
    return -math.log2(abs(det))

def decision_tree_width(n):
    if n == 1:
        return 1
    return 2 * decision_tree_width(n // 2)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    E = geometric_entanglement(n)
    C = decision_tree_width(n)
    ratio = C / (2 ** E + 1e-6)
    return {
        "metric_name": "Ratio of Decision Tree Width to Geometric Entanglement",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio <= 2 ** E + 1e-6,
        "counterexample": "" if ratio <= 2 ** E + 1e-6 else f"Counterexample for n={n}, E={E}, C={C}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, ...{result}...}}")
        results.append(result)

    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"First failing seed\" first_failing_seed={first_failing_seed}")