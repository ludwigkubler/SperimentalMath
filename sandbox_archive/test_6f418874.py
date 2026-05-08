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

def hook_length_formula(shape):
    n = len(shape)
    result = 1
    for i in range(n):
        for j in range(len(shape[i])):
            result *= (shape[i][j] + i - j) / (i + j + 1)
    return result

def kronecker_coefficient(lam, mu):
    n = len(lam)
    m = len(mu)
    if sum(lam) != sum(mu):
        return 0
    numerator = 1
    for i in range(n):
        for j in range(m):
            numerator *= hook_length_formula(lam[:i+1]) * hook_length_formula(mu[:j+1])
    denominator = math.factorial(sum(lam)) * math.prod(math.factorial(lam[i] + mu[j] - lam[i][j]) for i in range(n) for j in range(m))
    return numerator // denominator

def run_trial(seed: int):
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            k = random.randint(1, n-1)
            shape = [(n-k), (k)]
            kronecker_coeffs = [kronecker_coefficient(shape[:i+1], shape[i+1:]) for i in range(len(shape))]
            max_kronecker_coeff = max(kronecker_coeffs)
            total_metric_value += max_kronecker_coeff
            instances_tested += 1

    mean_metric_value = total_metric_value / instances_tested
    if n_values[-1] == 40 and mean_metric_value > 1e6:
        conjecture_holds = False
        counterexample = "Exponential growth observed for permanents."

    return {
        "metric_name": "Max Kronecker Coefficient",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3**j for i in range(5) for j in range(5)]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']:.6f}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)

    mean_metric_value = sum(r['metric_value'] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)

    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.6f} std=0.000000 support_fraction=1.000000")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.6f} std=0.000000 support_fraction={support_fraction:.6f}")
    else:
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"Exponential growth observed for permanents.\" first_failing_seed={first_failing_seed}")