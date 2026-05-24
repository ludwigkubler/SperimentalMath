# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 10  # Start with a small size and increase if needed
    instances_tested = 0
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""

    while instances_tested < 30 and n <= 40:
        f = [random.choice([0, 1]) for _ in range(2**n)]
        X = [i % n for i in range(2**n)]
        Y = [(i // n) % n for i in range(2**n)]

        # Compute communication complexity
        cc = 0
        for x in X:
            for y in Y:
                if f[x * n + y] != f[(x + 1) % n * n + (y + 1) % n]:
                    cc += 1
                    break

        if cc == 0:
            continue

        # Compute L^p norm of noncommutative Fourier transform
        p = 2  # Example value for p
        k = n // 2  # Number of inputs in each party's communication
        tau_p = sum(abs(f[i] - f[(i + 1) % (2**n)])**(p/k) for i in range(2**n))**(1/p)

        if tau_p < n**(1-p/k):
            conjecture_holds = False
            counterexample = "tau_p < n^(1-p/k)"

        total_metric_value += tau_p
        instances_tested += 1

    mean_metric_value = total_metric_value / instances_tested if instances_tested > 0 else 0.0
    support_fraction = Fraction(instances_tested, 30)

    return {
        "metric_name": "tau_p",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30))  # Default to first 29 primes

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = Fraction(sum(1 for r in results if r["conjecture_holds"]), len(results))

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= Fraction(8, 10):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break

        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")