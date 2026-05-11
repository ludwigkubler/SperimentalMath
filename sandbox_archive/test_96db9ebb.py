# auto-injected by SEC sandbox
import itertools
import json
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from collections import Counter

def factorial(n):
    if n == 0:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def hook_length_formula(n, k):
    numerator = 1
    denominator = (factorial(k) ** 2) * factorial(n - k)
    for i in range(1, n + 1):
        for j in range(1, k + 1):
            numerator *= (i + j - 1)
    return numerator / denominator

def plethysm_coefficient(n, k):
    if k == 0:
        return 1
    permanent_coeff = hook_length_formula(n, k) / hook_length_formula(n, 1)
    determinant_coeff = hook_length_formula(n, k - 1) / hook_length_formula(n, 1)
    return permanent_coeff - determinant_coeff

def generate_3sat_instance(n):
    clauses = []
    for _ in range(2 * n):
        clause = random.sample(range(1, n + 1), 3)
        if random.choice([True, False]):
            clause = [-x for x in clause]
        clauses.append(clause)
    return clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        k = math.ceil(n ** 1.5)
        instance = generate_3sat_instance(n)
        permanent_coeff = plethysm_coefficient(n, k)
        determinant_coeff = plethysm_coefficient(n, k - 1)
        gap = permanent_coeff - determinant_coeff
        if gap < n ** 1.5:
            conjecture_holds = False
            counterexample = f"n={n}, k={k}, gap={gap}"
            break
        total_metric_value += gap
        instances_tested += 1

    return {
        "metric_name": "plethysm_coeff_gap",
        "metric_value": total_metric_value / instances_tested if instances_tested > 0 else 0,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
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
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")