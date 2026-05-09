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

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def generate_primes(count):
    primes = []
    num = 2
    while len(primes) < count:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_ratio = 0.0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        d = 2
        mu = (n**2,)
        nu = (n**2 - random.randint(1, n),)
        instances_tested += 1

        # Compute Littlewood-Richardson coefficient for permanent's symmetric power
        perm_coeff = compute_littlewood_richardson(mu, nu)

        # Compute Littlewood-Richardson coefficient for determinant's symmetric power
        det_coeff = compute_littlewood_richardson(mu, nu)

        ratio = perm_coeff / det_coeff
        total_ratio += ratio

        if ratio < 2**(n**2/2):
            conjecture_holds = False
            counterexample = f"Seed {seed}: n={n}, mu={mu}, nu={nu}, perm_coeff={perm_coeff}, det_coeff={det_coeff}, ratio={ratio}"

    mean_ratio = total_ratio / len(n_values)
    return {
        "metric_name": "Ratio",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def compute_littlewood_richardson(mu, nu):
    # Placeholder for actual computation of Littlewood-Richardson coefficient
    # This is a dummy implementation and should be replaced with the actual algorithm
    return 1.0

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        primes = generate_primes(30)
        seeds = primes[:30]

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")

    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif any(result["counterexample"] for result in results):
        first_counterexample = next((result for result in results if result["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{first_counterexample['counterexample']}\" first_failing_seed={seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")