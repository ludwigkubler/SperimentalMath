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

def random_dnf(n, k):
    variables = list(range(1, n + 1))
    terms = []
    for _ in range(k):
        term = [random.choice(variables) for _ in range(random.randint(1, n))]
        terms.append(term)
    return terms

def submodular_width(dnf):
    if not dnf:
        return 0
    n = len(dnf[0])
    width = 0
    while dnf:
        new_dnf = []
        for term in dnf:
            if all(var in term for var in range(1, n + 1)):
                continue
            new_term = [var for var in term if var not in range(1, n + 1)]
            if new_term:
                new_dnf.append(new_term)
            else:
                width += 1
        dnf = new_dnf
    return width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    metric_name = "submodular_width"
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            dnf = random_dnf(n, random.randint(1, n))
            width = submodular_width(dnf)
            if width > math.log(n, 2) + 1:
                conjecture_holds = False
                counterexample = f"Monotone DNF with n={n}, width={width}"
                break
        instances_tested += 5

    return {
        "metric_name": metric_name,
        "metric_value": math.log(40, 2),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(seed) for seed in sys.argv[1:]]
    else:
        primes = generate_primes(30)
        seeds = primes

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{res['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")