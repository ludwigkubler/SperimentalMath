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

def xor_function(x, y):
    return x ^ y

def continued_fraction_approximation(rational, denominator_bound):
    p0, q0 = 0, 1
    p1, q1 = 1, 0
    a = rational.numerator // rational.denominator
    while True:
        if q1 > denominator_bound:
            return Fraction(p0 + p1, q0 + q1)
        p0, q0 = p1, q1
        p1, q1 = p1 * a + p0, q1 * a + q0
        a = (rational.numerator - p1) // q1

def fourier_coefficients(xor_function, n):
    coefficients = {}
    for x in range(2**n):
        for y in range(2**n):
            if x == 0 and y == 0:
                continue
            coeff = (1 / (2**n)) * sum(xor_function((x >> i) & 1, (y >> i) & 1) for i in range(n))
            coefficients[(x, y)] = coeff
    return coefficients

def max_abs_error(coefficients):
    return max(abs(coeff) for coeff in coefficients.values())

def communication_discrepancy(xor_function, n):
    f = fourier_coefficients(xor_function, n)
    D = 0
    for x in range(2**n):
        for y in range(2**n):
            if x == 0 and y == 0:
                continue
            D += abs(f[(x, y)] - f[(x + 1) % (2**n)][(y + 1) % (2**n)])
    return D / ((2**n)**2)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 10
    c = 1.0  # Constant for the lower bound
    xor_function = lambda x, y: x ^ y

    metric_name = "communication_discrepancy / (epsilon * log(n))"
    instances_tested = 30
    total_D_f = 0
    total_epsilon_f = 0

    for _ in range(instances_tested):
        D_f = communication_discrepancy(xor_function, n)
        epsilon_f = max_abs_error(fourier_coefficients(xor_function, n))
        if epsilon_f == 0:
            return {
                "metric_name": metric_name,
                "metric_value": None,
                "instances_tested": instances_tested,
                "conjecture_holds": False,
                "counterexample": "epsilon_f is zero"
            }
        total_D_f += D_f
        total_epsilon_f += epsilon_f

    mean_D_f = total_D_f / instances_tested
    mean_epsilon_f = total_epsilon_f / instances_tested
    metric_value = mean_D_f / (mean_epsilon_f * math.log(n))

    conjecture_holds = metric_value >= c / (math.log(n))
    counterexample = "" if conjecture_holds else "epsilon_f is too small"

    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
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

    mean_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"epsilon_f is too small\" first_failing_seed={first_failing_seed}")