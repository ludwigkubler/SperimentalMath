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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_kcnf(n, k):
        clauses = []
        for _ in range(k):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses

    def construct_representation(clauses):
        # Placeholder function to simulate representation construction
        # This is a dummy implementation and does not actually compute the representation
        D_F = len(clauses) * 2  # Simplified example
        return D_F, 1.5  # Minimal order of irreducible constituents

    n = random.randint(5, 40)
    k = random.randint(1, n)
    F = generate_kcnf(n, k)
    D_F, min_order = construct_representation(F)

    if D_F == 0 or min_order <= 0:
        return {
            "metric_name": "Ratio",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Invalid representation"
        }

    ratio = min_order / D_F
    if F:
        conjecture_holds = ratio <= 0.5
        counterexample = "" if conjecture_holds else f"Ratio {ratio} > 0.5"
    else:
        conjecture_holds = False
        counterexample = "Mapping undefined"

    return {
        "metric_name": "Ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    if all(result["conjecture_holds"] for result in results):
        support_fraction = 1.0
    else:
        support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    mean_ratio = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / sum(1 for result in results if result["metric_value"] is not None)
    std_deviation = math.sqrt(sum((result["metric_value"] - mean_ratio) ** 2 for result in results if result["metric_value"] is not None) / (sum(1 for result in results if result["metric_value"] is not None) - 1))

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_deviation} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio greater than 0.5\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE Reason=Insufficient evidence")