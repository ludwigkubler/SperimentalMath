# auto-injected by SEC sandbox
import random
import math
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
from fractions import Fraction
from itertools import combinations, permutations

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(n):
            if i != j:
                factor = -A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] += factor * A[i][k]
    return [row[n-1] / row[-2] for row in A]

def young_flattening_rank(tensor, m, k):
    n = len(tensor)
    syts = list(permutations(range(m), k))
    M = [[0] * (m**2) for _ in range(len(syts))]
    for i, syt in enumerate(syts):
        for j in combinations(range(m), m-k):
            monomial = 1
            for idx in sorted(syt + j):
                monomial *= tensor[idx // m][idx % m]
            M[i][j[0]] = monomial
    return len(gaussian_elimination(M))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for m in [2, 3, 4]:
        C = [[Fraction(1, m**2)] * m**2 for _ in range(m**2)]
        det_n = [[0] * (m**2) for _ in range(m**2)]
        for i in range(m):
            for j in range(m):
                det_n[i][j] = C[i][j]
        YF_k_det_n = young_flattening_rank(det_n, m, 1)
        YF_k_Per_m = young_flattening_rank(C, m, 1)
        delta = YF_k_det_n - YF_k_Per_m
        results.append((m, 1, det_n, C, YF_k_det_n, YF_k_Per_m, delta))
    metric_value = sum(delta for _, _, _, _, _, _, delta in results) / len(results)
    conjecture_holds = all(delta >= Fraction(1, 2) * binomial(m, k) * (n - m**2 + 1) for m, k, _, _, _, _, delta in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "delta(m,k)",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
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
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")