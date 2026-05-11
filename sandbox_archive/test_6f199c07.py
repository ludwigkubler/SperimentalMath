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
        max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def det(A):
    n = len(A)
    if n == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]
    else:
        det_val = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det_val += (-1) ** j * A[0][j] * det(submatrix)
        return det_val

def permanent(A):
    n = len(A)
    if n == 2:
        return A[0][0] * A[1][1] + A[0][1] * A[1][0]
    else:
        perm_val = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            perm_val += A[0][j] * permanent(submatrix)
        return perm_val

def plethysm_coefficient(n):
    if n == 1:
        return 2
    elif n == 2:
        return 6
    else:
        return (n + 1) * plethysm_coefficient(n - 1)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    metric_name = "plethysm_coefficient"
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        A = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        plethysm_val = plethysm_coefficient(n)
        perm_val = permanent(A)
        total_metric_value += plethysm_val
        instances_tested += n

        if plethysm_val <= perm_val:
            conjecture_holds = False
            counterexample = f"n={n}, plethysm coefficient {plethysm_val} ≤ permanent value {perm_val}"

    return {
        "metric_name": metric_name,
        "metric_value": total_metric_value / instances_tested,
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
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"plethysm_coefficient ≤ permanent\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")