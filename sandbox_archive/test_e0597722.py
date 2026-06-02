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

def generate_k_cnf(n, k):
    clauses = set()
    while len(clauses) < k:
        clause = tuple(random.sample(range(1, n + 1), 2))
        if clause not in clauses and -clause not in clauses:
            clauses.add(clause)
    return clauses

def hopf_algebroid_representation(k_cnf):
    # Construct a simple representation for demonstration
    # This is a placeholder and should be replaced with actual computation
    return len(k_cnf)

def frege_proof_length(k_cnf):
    # Placeholder function to simulate Frege proof length calculation
    return len(k_cnf) * 10

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0.0
    instances_tested = 0
    min_crossed_products = float('inf')
    max_crossed_products = 0

    for n in n_values:
        k_cnf = generate_k_cnf(n, random.randint(1, n))
        crossed_products = hopf_algebroid_representation(k_cnf)
        proof_length = frege_proof_length(k_cnf)

        if crossed_products == 0 or proof_length == 0:
            continue

        instances_tested += 1
        total_metric_value += proof_length / crossed_products
        min_crossed_products = min(min_crossed_products, crossed_products)
        max_crossed_products = max(max_crossed_products, crossed_products)

    if instances_tested < 30:
        return {
            "metric_name": "Ratio of Frege Proof Length to Crossed Products",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "Insufficient instances tested"
        }

    mean_metric_value = total_metric_value / instances_tested
    ratio_threshold = 2.0
    support_fraction = sum(1 for n in n_values if min_crossed_products <= max_crossed_products * ratio_threshold) / len(n_values)

    return {
        "metric_name": "Ratio of Frege Proof Length to Crossed Products",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"Ratio out of [0.5, {ratio_threshold}] for n={max(n_values)}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=NA support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=NA support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio out of [0.5, 2]\" first_failing_seed={first_failing_seed}")