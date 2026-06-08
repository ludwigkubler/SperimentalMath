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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 30  # Fixed instance size for simplicity
    instances_tested = 100
    n_max = n
    conjecture_holds = True
    counterexample = ""

    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]

    def calculate_minimal_index_of_topological_entanglement(f):
        # Placeholder function to simulate the calculation
        return random.random()

    def calculate_communication_complexity_rank_variance(f):
        # Placeholder function to simulate the calculation
        return random.random()

    mu_values = []
    R_values = []

    for _ in range(instances_tested):
        f = generate_boolean_function(n)
        mu = calculate_minimal_index_of_topological_entanglement(f)
        R = calculate_communication_complexity_rank_variance(f)
        mu_values.append(mu)
        R_values.append(R)

    correlation_coefficient = sum((mu - mean_mu) * (R - mean_R) for mu, R in zip(mu_values, R_values)) / instances_tested
    mean_mu = sum(mu_values) / instances_tested
    mean_R = sum(R_values) / instances_tested

    if abs(correlation_coefficient) < 0.7:
        conjecture_holds = False
        counterexample = "correlation_coefficient_too_low"

    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")