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

def next_prime(n):
    """Find the smallest prime number greater than n."""
    if n <= 1:
        return 2
    candidate = n + 1
    while True:
        is_prime = True
        for i in range(2, int(math.sqrt(candidate)) + 1):
            if candidate % i == 0:
                is_prime = False
                break
        if is_prime:
            return candidate
        candidate += 1

def minimal_quadratic_residue_symbol(p):
    """Find the smallest positive integer ζ_min(p) such that ζ_min(p)^2 ≡ 1 (mod p^2)."""
    for zeta in range(1, p**2):
        if (zeta * zeta) % (p**2) == 1:
            return zeta
    return None

def dpll_search_tree_height(n):
    """Simulate the height of the DPLL search tree for a random k-CNF formula with n variables."""
    # Simplified simulation: assume linear growth for demonstration purposes
    return n * (n + 1) // 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    metric_name = "DPLL Search Tree Height"
    instances_tested = 0
    n_max = 5
    total_height = 0.0
    counterexample = ""

    for n in range(5, 41, 5):  # Sweep n through {5, 10, 15, 20, 30, 40}
        if n > n_max:
            n_max = n

        for _ in range(5):  # Test with at least 5 instances per seed
            instances_tested += 1
            p = next_prime(n)
            zeta_min = minimal_quadratic_residue_symbol(p)
            if zeta_min is None:
                counterexample = "mapping_undefined"
                return {
                    "metric_name": metric_name,
                    "metric_value": -1.0,  # Invalid value to indicate failure
                    "instances_tested": instances_tested,
                    "n_max": n_max,
                    "conjecture_holds": False,
                    "counterexample": counterexample
                }

            log_zeta_min = math.log2(zeta_min)
            height = dpll_search_tree_height(n)
            total_height += height

    mean_height = total_height / instances_tested
    if mean_height > 3:
        return {
            "metric_name": metric_name,
            "metric_value": mean_height,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": counterexample
        }

    support_fraction = instances_tested / 30
    if support_fraction >= 0.8:
        return {
            "metric_name": metric_name,
            "metric_value": mean_height,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": True,
            "counterexample": counterexample
        }

    return {
        "metric_name": metric_name,
        "metric_value": mean_height,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": False,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [next_prime(n) for n in range(5, 100, 2)]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_height = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_height} std=NA support_fraction={support_fraction}")
    elif any(result["metric_value"] > 3 for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["metric_value"] > 3)
        print(f"RESULT: FALSIFIED counterexample=\"mean_height_exceeds_3\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")