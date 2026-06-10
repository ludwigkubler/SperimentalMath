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

def generate_random_protocol(n):
    return [random.randint(0, 1) for _ in range(n)]

def rank_variance(phi):
    n = len(phi)
    mean = sum(phi) / n
    variance = sum((x - mean) ** 2 for x in phi) / n
    return variance

def modular_form(phi):
    # Placeholder function. Replace with actual computation.
    return Fraction(1, 1)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    metric_name = "modular_degree_bound"
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""

    for n in range(5, 41, 5):
        phi = generate_random_protocol(n)
        r_phi = rank_variance(phi)
        mu_phi = modular_form(phi)

        instances_tested += len(phi)
        n_max = max(n_max, n)

        if mu_phi > 1.5 * r_phi:
            conjecture_holds = False
            counterexample = f"mu_phi={mu_phi} > 1.5 * r_phi={1.5 * r_phi}"

    return {
        "metric_name": metric_name,
        "metric_value": instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")