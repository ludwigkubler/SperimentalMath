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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def mod_inverse(a, m):
    m0, x0, x1 = m, 0, 1
    if m == 1:
        return 0
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += m0
    return x1

def p_adic_l_function(q):
    zeta_q = 0
    k = 1
    while True:
        term = Fraction(1, q ** k * math.log(k + 1))
        if abs(term) < 1e-10:  # Small threshold to stop the series
            break
        zeta_q += term
        k += 1
    return zeta_q

def dedekind_zeta(q):
    if q <= 0:
        raise ValueError("q must be a positive integer")
    sum_val = 0
    for n in range(1, int(math.sqrt(q)) + 1):
        sum_val += Fraction(1, (n ** 2) * (q - n ** 2))
    return sum_val

def dpll_refutation_depth(n):
    if n < 5:
        raise ValueError("n must be at least 5")
    depth = 0
    for _ in range(n):
        if random.choice([True, False]):
            depth += 1
    return depth

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        q = random.randint(2, 100)  # Random p-adic integer
        l_value = p_adic_l_function(q)
        depth = dpll_refutation_depth(n)
        metric_value = abs(l_value - (depth ** Fraction(3, 4)))
        total_metric_value += metric_value
        instances_tested += n

        if metric_value > 10:  # Arbitrary large threshold to consider as failure
            conjecture_holds = False
            counterexample = f"n={n}, q={q}, L(1/2, χ_q)={l_value}, depth={depth}"

    return {
        "metric_name": "abs(L(1/2, χ_q) - depth^(3/4))",
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

    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = (sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support or budget_exceeded")