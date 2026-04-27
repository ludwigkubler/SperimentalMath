# auto-injected by SEC sandbox
import itertools
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math

def gaussian_elimination(A):
    n = len(A)
    m = len(A[0])
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        if A[i][i] == 0:
            return None  # Singular matrix
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(m):
                A[j][k] -= factor * A[i][k]
    rank = sum(1 for row in A if any(row))
    return rank

def boundary_matrix(f, n):
    m = 2**n
    B = [[0]*m for _ in range(n)]
    for i in range(m):
        mask = i
        while mask:
            B[bin(mask).count('1')-1][i] = f[i]
            mask &= (mask - 1)
    return B

def betti_numbers(B, n):
    betti = [0]*n
    for k in range(n):
        ker_dim = gaussian_elimination(B[:k+1])
        if ker_dim is None:
            return None  # Singular matrix
        rank = sum(1 for row in B[k] if any(row))
        betti[k] = ker_dim - rank
    return betti

def dnf_min(f, n):
    m = 2**n
    prime_implicants = []
    for i in range(m):
        mask = i
        while mask:
            if all(f[j] == f[i] for j in range(m) if (j & mask) == mask):
                prime_implicants.append(mask)
            mask &= (mask - 1)
    cover = set()
    for implicant in prime_implicants:
        cover |= {i for i in range(m) if implicant & i == implicant}
    return len(cover)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 8, 11, 14]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(20):
            f = ''.join(str(random.randint(0, 1)) for _ in range(2**n))
            if f.count('1') == 0 or f.count('1') == 2**n:
                continue
            B = boundary_matrix(f, n)
            betti = betti_numbers(B, n)
            if betti is None:
                conjecture_holds = False
                counterexample = "singular_matrix"
                break
            DNF_min_val = dnf_min(f, n)
            metric_value = math.ceil(math.log2(DNF_min_val)) - sum(betti)
            total_metric_value += metric_value
            instances_tested += 1

    mean_metric_value = total_metric_value / instances_tested if instances_tested > 0 else 0
    support_fraction = instances_tested / (len(n_values) * 20)

    return {
        "metric_name": "Betti Sum - DNF Min",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")