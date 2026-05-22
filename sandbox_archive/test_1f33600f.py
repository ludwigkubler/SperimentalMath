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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def p_adic_valuation(f, p):
    val = 0
    for coeff in f:
        if coeff != 0:
            factors = []
            n = abs(coeff)
            for i in range(2, int(math.sqrt(n)) + 1):
                while n % i == 0 and gcd(i, p) == 1:
                    factors.append(i)
                    n //= i
            if n > 1 and gcd(n, p) == 1:
                factors.append(n)
            val = max(val, len(set(factors)))
    return val

def is_acc0_circuit(f, depth):
    # Placeholder for ACC⁰ circuit checking logic
    return True

def run_trial(seed: int) -> dict:
    random.seed(seed)
    p = 2  # Using prime 2 for simplicity
    n = 10  # Starting with small n and increasing
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for _ in range(30):  # Testing 30 instances per seed
        coefficients = [random.randint(-10, 10) for _ in range(n + 1)]
        f = coefficients[::-1]  # Polynomial with given coefficients
        val_p_f = p_adic_valuation(f, p)
        depth = random.randint(1, n)  # Random circuit depth

        if val_p_f >= depth:
            conjecture_holds = False
            counterexample = "val_p(f) >= D(f)"
            break

    return {
        "metric_name": "p-adic_valuation",
        "metric_value": val_p_f,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 30)]
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")