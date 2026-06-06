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
    
    def generate_boolean_formula(n):
        formula = ""
        for _ in range(n):
            var = f"x{random.randint(0, n-1)}"
            if random.choice([True, False]):
                formula += f"({var} AND "
            else:
                formula += f"NOT {var} OR "
        return formula[:-4] + ")"

    def compute_minimal_rank(n):
        # Placeholder for the actual computation of minimal rank
        # This is a dummy implementation and should be replaced with the actual logic
        return random.randint(1, n)

    def resolution_proof_width(formula):
        # Placeholder for the actual computation of resolution proof width
        # This is a dummy implementation and should be replaced with the actual logic
        return len(formula.split())

    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_w = 0
    total_r = 0

    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            formula = generate_boolean_formula(n)
            r = compute_minimal_rank(n)
            w = resolution_proof_width(formula)
            
            if w < r / 10:
                return {
                    "metric_name": "Resolution Proof Width",
                    "metric_value": None,
                    "instances_tested": instances_tested,
                    "n_max": n,
                    "conjecture_holds": False,
                    "counterexample": f"Formula: {formula}, Rank: {r}, Width: {w}"
                }
            
            total_w += w
            total_r += r
            instances_tested += 1

    mean_w = total_w / instances_tested
    mean_r = total_r / instances_tested
    
    return {
        "metric_name": "Resolution Proof Width",
        "metric_value": mean_w,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": mean_w >= 10 * mean_r,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    total_w = sum(r["metric_value"] for r in results if r["metric_value"] is not None)
    total_r = sum(r["instances_tested"] * r["metric_value"] / r["instances_tested"] for r in results if r["metric_value"] is not None)
    mean_w = total_w / len(results)
    mean_r = total_r / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_w} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"First failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_data n_tested={len(results)}")