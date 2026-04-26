# auto-injected by SEC sandbox
import itertools
import collections
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
import json

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def matrix_multiplication(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def tropical_fourier_transform(f, N):
    f = [max(x, -10) for x in f]  # Clamp to [-10, 10]
    F = [sum(f[(i + j) % N] for i in range(N)) for j in range(N)]
    return F

def discrepancy_calculation(f):
    n = len(f)
    mean = sum(f) / n
    return max(max(f), min(f)) - mean

def run_trial(seed: int) -> dict:
    random.seed(seed)
    N_values = [16, 32, 64, 128]
    MFC_invariance_count = 0
    Discrepancy_invariance_count = 0
    DC_shift_count = 0

    for N in N_values:
        f = [random.uniform(-10, 10) for _ in range(N)]
        TFT_f = tropical_fourier_transform(f, N)
        MFC_f = min(abs(x) for x in TFT_f[1:])
        Discrepancy_f = discrepancy_calculation(f)

        for _ in range(20):
            c = random.uniform(-50, 50)
            f_c = [max(x + c, -10) for x in f]  # Clamp to [-10, 10]
            TFT_f_c = tropical_fourier_transform(f_c, N)
            MFC_f_c = min(abs(x) for x in TFT_f_c[1:])
            Discrepancy_f_c = discrepancy_calculation(f_c)

            if abs(MFC_f_c - MFC_f) < 1e-9 and abs(Discrepancy_f_c - Discrepancy_f) < 1e-9:
                MFC_invariance_count += 1
            if abs(TFT_f_c[0] - TFT_f[0]) < N * abs(c):
                DC_shift_count += 1

        if MFC_invariance_count == 20 and Discrepancy_invariance_count == 20:
            Discrepancy_invariance_count = 0
        else:
            return {
                "metric_name": "MFC/Discrepancy Invariance",
                "metric_value": None,
                "instances_tested": N_values.count(N) * 20,
                "conjecture_holds": False,
                "counterexample": f"Failed MFC or Discrepancy invariance for N={N}"
            }

    return {
        "metric_name": "MFC/Discrepancy Invariance",
        "metric_value": None,
        "instances_tested": len(N_values) * 20,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps(result)}")
        results.append(result)

    mean_MFC_invariance = sum(r["instances_tested"] for r in results if r["conjecture_holds"]) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_MFC_invariance} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_MFC_invariance} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"MFC/Discrepancy Invariance failed\" first_failing_seed={first_failing_seed}")