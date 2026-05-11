# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from itertools import combinations

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def factorial(n):
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def hook_length_formula(shape):
    m, n = len(shape), len(shape[0])
    total = 1
    for i in range(m):
        for j in range(n):
            h = shape[i][j] - (i + 1) - (n - j)
            total *= h + 1
            total //= (i + 1) * (j + 1)
    return total

def permanent(tensor):
    if len(tensor) == 0:
        return 1
    n = len(tensor)
    result = 0
    for perm in combinations(range(n), n):
        sign = (-1) ** sum(i < j for i, j in enumerate(perm))
        product = 1
        for i in range(n):
            product *= tensor[i][perm[i]]
        result += sign * product
    return result

def determinant(tensor):
    if len(tensor) == 0:
        return 1
    n = len(tensor)
    result = 0
    for perm in combinations(range(n), n):
        sign = (-1) ** sum(i < j for i, j in enumerate(perm))
        product = 1
        for i in range(n):
            product *= tensor[i][perm[i]]
        result += sign * product
    return result

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(1, min(n**2 // 3, 20))
    variables = list(range(n))
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, 3)
        clauses.append(clause)

    permanent_tensor = [[0] * n for _ in range(n)]
    determinant_tensor = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if (i + 1) % 2 == (j + 1) % 2:
                permanent_tensor[i][j] = 1
            else:
                permanent_tensor[i][j] = -1

    for i in range(n):
        for j in range(n):
            if (i + 1) % 2 == (j + 1) % 2:
                determinant_tensor[i][j] = 1
            else:
                determinant_tensor[i][j] = -1

    permanent_value = permanent(permanent_tensor)
    determinant_value = determinant(determinant_tensor)

    return {
        "metric_name": "Multiplicity Gap",
        "metric_value": abs(permanent_value - determinant_value),
        "instances_tested": 1,
        "conjecture_holds": abs(permanent_value - determinant_value) >= n**1.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30)) + list(range(101, 130))
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)

    mean_metric = sum(r["metric_value"] for r in results) / len(results)
    std_metric = (sum((r["metric_value"] - mean_metric) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")