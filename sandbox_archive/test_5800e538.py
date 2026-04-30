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

def fast_walsh_hadamard_transform(f):
    n = len(f)
    if n == 1:
        return f
    even = fast_walsh_hadamard_transform([f[i] for i in range(0, n, 2)])
    odd = fast_walsh_hadamard_transform([f[i] for i in range(1, n, 2)])
    result = [0] * n
    for k in range(n // 2):
        result[k] = even[k] + odd[k]
        result[k + n // 2] = even[k] - odd[k]
    return result

def log_rank(matrix):
    m, n = len(matrix), len(matrix[0])
    rank = 0
    for i in range(m):
        pivot_row = None
        for j in range(i, m):
            if any(matrix[j][k] != 0 for k in range(n)):
                pivot_row = j
                break
        if pivot_row is None:
            continue
        rank += 1
        for j in range(m):
            if j == pivot_row:
                continue
            factor = matrix[j][i] / matrix[pivot_row][i]
            for k in range(n):
                matrix[j][k] -= factor * matrix[pivot_row][k]
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 5
    c = 10  # Constant to check the inequality D(f) >= c/λ
    instances_tested = 30
    total_metric_value = 0
    conjecture_holds = True
    counterexample = ""

    for _ in range(instances_tested):
        f = [random.randint(0, 1) for _ in range(2**n)]
        fourier_coeffs = fast_walsh_hadamard_transform(f)
        lambda_max = max(abs(coeff) for coeff in fourier_coeffs)
        if lambda_max == 0:
            continue
        communication_matrix = [[f[i ^ j] for j in range(2**n)] for i in range(2**n)]
        D_f = log_rank(communication_matrix)
        total_metric_value += D_f / (c * lambda_max)
        if D_f < c / lambda_max:
            conjecture_holds = False
            counterexample = f"Function with λ={lambda_max} and D(f)={D_f}"

    return {
        "metric_name": "D(f)/λ",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and not counterexample:
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={seeds[results.index(next(r for r in results if not r['conjecture_holds']))]}")
    elif any(not r["conjecture_holds"] for r in results):
        print(f"RESULT: FALSIFIED counterexample=\"{next(r for r in results if not r['conjecture_holds'])['counterexample']}\" first_failing_seed={seeds[results.index(next(r for r in results if not r['conjecture_holds']))]}")
    else:
        print(f"RESULT: INCONCLUSIVE no seeds tested or all seeds inconclusive")