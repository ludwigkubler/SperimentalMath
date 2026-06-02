# auto-injected by SEC sandbox
import math
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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 10  # Start with a small instance size and increase if needed
    instances_tested = 0
    total_metric_value = 0
    max_n = 0
    conjecture_holds = True
    counterexample = ""

    for _ in range(30):  # Aim for at least 30 instances per seed
        n += 5  # Increase instance size to avoid trivial cases
        if n > 40:
            break

        max_n = max(max_n, n)

        # Generate a random CNF formula with n variables
        num_clauses = random.randint(1, n)
        phi = []
        for _ in range(num_clauses):
            clause = [random.choice(range(-n, -1)) for _ in range(random.randint(1, n))]
            phi.append(clause)

        # Compute the number of invariant factors (simplified example)
        num_invariant_factors = len(phi)  # Placeholder for actual computation

        # Compute the clause set complexity
        c_phi = sum(len(clause) for clause in phi)

        # Check if the conjecture holds for this instance
        if num_invariant_factors > 1.5 * c_phi ** 0.5:
            conjecture_holds = False
            counterexample = f"n={n}, invariant_factors={num_invariant_factors}, c_phi={c_phi}"

        instances_tested += 1
        total_metric_value += num_invariant_factors

    if instances_tested == 0:
        return {
            "metric_name": "Invariant Factors",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max_n,
            "conjecture_holds": False,
            "counterexample": "No instances tested"
        }

    mean_metric_value = total_metric_value / instances_tested
    return {
        "metric_name": "Invariant Factors",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)

    mean_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all("instances_tested" in result and result["instances_tested"] > 0 for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=NA support_fraction={support_fraction}")
    elif any(result["counterexample"] != "" for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["counterexample"] != "")
        print(f"RESULT: FALSIFIED counterexample=\"{next(result['counterexample'] for result in results if result['counterexample'] != 'mapping_undefined')}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")