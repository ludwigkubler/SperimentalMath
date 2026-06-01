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
    
    def generate_cnf(n):
        literals = [f"x{i}" for i in range(1, n+1)]
        clauses = []
        for _ in range(n):
            clause = random.sample(literals, 2)
            clauses.append(f"({clause[0]} OR {clause[1]})")
        return " AND ".join(clauses)

    def cnf_to_quadratic_number_field(cnf):
        # Simplified encoding of CNF to quadratic number field
        # This is a placeholder and should be replaced with actual encoding logic
        return random.randint(1, 100)

    def frege_proof_length(n):
        # Simplified estimation of Frege proof length
        # This is a placeholder and should be replaced with actual estimation logic
        return n * (n + 1) // 2

    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n)
            discriminant = cnf_to_quadratic_number_field(cnf)
            proof_length = frege_proof_length(n)
            if discriminant == 0:
                continue
            log_discriminant = math.log(discriminant)
            results.append((log_discriminant, proof_length))

    if not results:
        return {
            "metric_name": "log_delta",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "no_valid_discriminants"
        }

    log_discriminants = [r[0] for r in results]
    proof_lengths = [r[1] for r in results]

    n_max = max(n for _, n in results)
    instances_tested = len(results)

    if n_max < 16:
        return {
            "metric_name": "log_delta",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "n_max_too_small"
        }

    def linear_regression(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
        denominator = sum((xi - mean_x) ** 2 for xi in x)
        slope = numerator / denominator if denominator != 0 else None
        intercept = mean_y - slope * mean_x if slope is not None else None
        return slope, intercept

    slope, _ = linear_regression(log_discriminants, proof_lengths)
    r_squared = sum((yi - (slope * xi + intercept)) ** 2 for xi, yi in zip(log_discriminants, proof_lengths))
    r_squared /= sum((yi - mean_y) ** 2 for yi in proof_lengths)

    return {
        "metric_name": "log_delta",
        "metric_value": slope,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": r_squared >= 0.9 and p_value <= 0.01,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []

    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_supported\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_valid_discriminants")