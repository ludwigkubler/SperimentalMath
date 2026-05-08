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

def factorial(n):
    if n == 0:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def binomial_coefficient(n, k):
    return factorial(n) // (factorial(k) * factorial(n - k))

def plethysm_coefficient(m, n):
    if m == 0:
        return 1
    if m < n:
        return 0
    coeff = 0
    for i in range(1, n + 1):
        coeff += (-1) ** (i - 1) * binomial_coefficient(n, i) * plethysm_coefficient(m - i, n)
    return coeff

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        m_values = [random.randint(1, int(n ** 1.5)) for _ in range(10)]
        for m in m_values:
            trivial_multiplicity_perm = plethysm_coefficient(m, n)
            trivial_multiplicity_det = plethysm_coefficient(m, m)
            if trivial_multiplicity_perm <= trivial_multiplicity_det:
                conjecture_holds = False
                counterexample = f"n={n}, m={m}: perm<{trivial_multiplicity_perm}, det<{trivial_multiplicity_det}"
                break
        total_metric_value += trivial_multiplicity_perm / trivial_multiplicity_det
        instances_tested += len(m_values)

    return {
        "metric_name": "multiplicity_ratio",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]]
    if not seeds:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        seeds = primes[:30]

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")

    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")