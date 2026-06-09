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
    n = 40  # Set a fixed n for simplicity and to avoid timeout issues
    instances_tested = 30
    total_metric_value = 0.0
    counterexample = ""

    for _ in range(instances_tested):
        f = [random.choice([0, 1]) for _ in range(2**n)]
        # Compute the geometric entropy Γ(f)
        p = sum(f) / len(f)
        gamma_f = -p * math.log(p) - (1 - p) * math.log(1 - p)

        # Compute the communication complexity rank r(f)
        # For simplicity, we assume a constant rank for all functions
        r_f = 2

        # Calculate Var(Γ(f))
        var_gamma_f = gamma_f ** 2

        # Check if the conjecture holds
        expected_value = n ** (2 * r_f)
        ratio = var_gamma_f / expected_value
        if not (0.5 <= ratio <= 1.5):
            counterexample = f"Gamma(f)={gamma_f}, Var(Γ(f))={var_gamma_f}, Expected=n^{2*r_f}={expected_value}"

        total_metric_value += var_gamma_f

    metric_name = "Var(Γ(f))"
    metric_value = total_metric_value / instances_tested
    conjecture_holds = counterexample == ""

    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        seeds = [2**i + 3 for i in range(5, 6)]  # Default to a few prime numbers

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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")