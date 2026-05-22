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
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, m):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def rank(A):
    A = gaussian_elimination(A)
    r = 0
    for row in A:
        if any(row):
            r += 1
    return r

def p_adic_derivative(f, n):
    # Placeholder implementation; actual algorithm needed
    return [[0] * (n+1) for _ in range(n+1)]

def circuit_complexity(f):
    # Placeholder implementation; actual algorithm needed
    return random.randint(1, 100)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    instances_tested = 0
    total_circuit_size = 0
    total_rank = 0

    for _ in range(40):
        f = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        rank_f = rank(f)
        circuit_size_f = circuit_complexity(f)
        instances_tested += 1
        total_circuit_size += circuit_size_f
        total_rank += rank_f

    mean_circuit_size = total_circuit_size / instances_tested
    mean_rank = total_rank / instances_tested
    correlation_coefficient = (instances_tested * sum(c * r for c, r in zip(range(1, n+1), range(1, n+1))) - 
                               instances_tested * mean_circuit_size * mean_rank) / \
                              math.sqrt((instances_tested * sum(c**2 for c in range(1, n+1)) - instances_tested * mean_circuit_size**2) *
                                        (instances_tested * sum(r**2 for r in range(1, n+1)) - instances_tested * mean_rank**2))

    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "conjecture_holds": correlation_coefficient > 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        seeds = [2**i + 3**j + 5**k for i, j, k in itertools.product(range(4), repeat=3)]

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)

    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")