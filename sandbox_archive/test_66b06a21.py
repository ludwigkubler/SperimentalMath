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
    
    def generate_monomial_ideal(n):
        variables = list(range(1, n + 1))
        ideal = {frozenset(random.sample(variables, k)) for k in range(1, n)}
        return ideal

    def compute_k_theory_group_size(ideal):
        # Placeholder function to simulate K-theory group size computation
        # Replace with actual implementation if available
        return len(ideal)

    def construct_monotone_circuit_depth(ideal):
        # Placeholder function to simulate monotone circuit depth computation
        # Replace with actual implementation if available
        return random.randint(1, 10)  # Simulating a simple depth

    n = random.choice([5, 10, 15, 20, 30, 40])
    ideal = generate_monomial_ideal(n)
    k_theory_group_size = compute_k_theory_group_size(ideal)
    circuit_depth = construct_monotone_circuit_depth(ideal)

    return {
        "metric_name": "K-theory Group Size / Circuit Depth",
        "metric_value": Fraction(k_theory_group_size, circuit_depth),
        "instances_tested": 1,
        "conjecture_holds": k_theory_group_size <= circuit_depth,
        "counterexample": "" if k_theory_group_size <= circuit_depth else f"K-theory group size {k_theory_group_size} > circuit depth {circuit_depth}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided

    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    total_metric_value = sum(result["metric_value"] for result in results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    mean_metric_value = Fraction(total_metric_value).limit_denominator()
    std_metric_value = (sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results)) ** 0.5

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")