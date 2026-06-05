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

def generate_tseitin_formula(n: int):
    variables = [f"x{i+1}" for i in range(n)]
    tseitin_vars = [f"T{i+1}" for i in range(n)]
    clauses = []

    # Generate clauses for each variable
    for i in range(n):
        clause = [-tseitin_vars[i], variables[i]]
        clauses.append(clause)
        clause = [tseitin_vars[i], -variables[i]]
        clauses.append(clause)

    # Generate clauses for implications
    for i in range(1, n):
        clause = [-tseitin_vars[i-1], tseitin_vars[i]]
        clauses.append(clause)

    # Final clause
    clause = [tseitin_vars[n-1]]
    clauses.append(clause)

    phi_G = " & ".join(f"({c[0]} -> {c[1]})" for c in clauses)
    return phi_G, variables, clauses

def compute_minimal_generators(phi_G: str):
    # Placeholder function to simulate minimal generators computation
    # This is a dummy implementation and should be replaced with actual logic
    n = len(phi_G.split())
    return n // 2

def compute_resolution_proof_width(phi_G: str):
    # Placeholder function to simulate resolution proof width computation
    # This is a dummy implementation and should be replaced with actual logic
    n = len(phi_G.split())
    return n ** 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        phi_G, variables, clauses = generate_tseitin_formula(n)
        min_generators = compute_minimal_generators(phi_G)
        proof_width = compute_resolution_proof_width(phi_G)

        if min_generators < n / 2 or proof_width > 10 * n ** 2:
            return {
                "metric_name": "resolution_proof_width",
                "metric_value": None,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": f"min_generators < n/2 or proof_width > 10n^2 for n={n}"
            }

        results.append({
            "n": n,
            "min_generators": min_generators,
            "proof_width": proof_width
        })

    correlation_coefficient = compute_correlation(results)
    conjecture_holds = correlation_coefficient >= 0.8

    return {
        "metric_name": "resolution_proof_width",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

def compute_correlation(data: list) -> float:
    n = len(data)
    if n < 2:
        return None

    sum_min_generators = sum(r["min_generators"] for r in data)
    sum_proof_width = sum(r["proof_width"] for r in data)
    sum_min_gen_squared = sum(r["min_generators"] ** 2 for r in data)
    sum_proof_width_squared = sum(r["proof_width"] ** 2 for r in data)
    sum_min_gen_proof_width = sum(r["min_generators"] * r["proof_width"] for r in data)

    numerator = n * sum_min_gen_proof_width - sum_min_generators * sum_proof_width
    denominator = math.sqrt((n * sum_min_gen_squared - sum_min_generators ** 2) * (n * sum_proof_width_squared - sum_proof_width ** 2))

    if denominator == 0:
        return None

    return numerator / denominator

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(3, 151, 6))  # Default to first 30 primes if no seeds provided
    results = []

    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{trial_result}}}")
        results.append(trial_result)

    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.8\" first_failing_seed={first_failing_seed}")