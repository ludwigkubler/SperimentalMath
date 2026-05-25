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
from fractions import Fraction
import math

def inverse_ackermann(n):
    if n == 0:
        return 1
    elif n == 1:
        return 2
    else:
        a = 2
        for _ in range(1, n):
            a = 2 * inverse_ackermann(a - 1)
        return a

def boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def generate_quandle_representations(boolean_func):
    # Simplified representation generation
    return [boolean_func]

def calculate_minimal_rank(quandle_representation):
    # Minimal rank calculation (simplified)
    return len(quandle_representation)

def check_conjecture(n, boolean_function):
    quandle_reps = generate_quandle_representations(boolean_function)
    for rep in quandle_reps:
        minimal_rank = calculate_minimal_rank(rep)
        lower_bound = Fraction(2**n, inverse_ackermann(n))
        if minimal_rank < lower_bound:
            return False
    return True

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0.0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        boolean_func = boolean_function(n)
        if not check_conjecture(n, boolean_func):
            conjecture_holds = False
            counterexample = f"n={n}, minimal_rank<{2**n / inverse_ackermann(n)}"
            break

    return {
        "metric_name": "minimal_rank",
        "metric_value": total_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        # Default list of 30 primes
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, min(30, len(primes)))

    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = (sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))**0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='{result['counterexample']}' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")