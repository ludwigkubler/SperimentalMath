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

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        max_row = i
        for k in range(i+1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i+1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = Fraction(b[i], A[i][i])
        for k in range(i-1, -1, -1):
            b[k] -= A[k][i] * x[i]
    return x

def minimal_tropical_motivic_rank(A, b):
    n = len(b)
    x = gaussian_elimination(A, b)
    mtr_P = 0
    for i in range(n):
        if all(A[i][j] * x[j] <= b[i] for j in range(n)):
            mtr_P += 1
    return mtr_P

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 0
    total_metric_value = 0.0
    support_count = 0
    counterexample = ""

    for N in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Test each size 5 times to ensure statistical signal
            ε = random.uniform(1e-6, 1e-2)
            A = [[random.randint(-10, 10) for _ in range(N)] for _ in range(N)]
            b = [random.randint(-10, 10) for _ in range(N)]
            mtr_P = minimal_tropical_motivic_rank(A, b)
            instances_tested += 1
            total_metric_value += mtr_P

            if mtr_P <= math.log(N) / math.log(1/ε):
                support_count += 1
            else:
                counterexample = f"mtr(P)={mtr_P} > log({N}) / log(1/{ε})"
                break

    mean_metric_value = total_metric_value / instances_tested
    conjecture_holds = support_count == instances_tested

    return {
        "metric_name": "minimal_tropical_motivic_rank",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")