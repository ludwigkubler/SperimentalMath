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
    
    def communication_complexity(f, M):
        return len(f) * len(M)

    def generate_symplectic_manifold(n):
        # Simplified generation of a symplectic manifold with n elements
        return list(range(1, n + 1))

    def evaluate_polynomial(poly, M):
        result = 0
        for term in poly:
            product = 1
            for var in term:
                product *= M[var - 1]
            result += product
        return result

    def generate_random_poly(n):
        # Generate a random polynomial of degree n
        return [random.randint(1, 5) for _ in range(n)]

    instances_tested = 0
    total_comm_complexity = 0
    n_max = 0

    for n in {5, 10, 15, 20, 30, 40}:
        M = generate_symplectic_manifold(n)
        f = generate_random_poly(n)
        comm_complexity = communication_complexity(f, M)
        total_comm_complexity += comm_complexity
        instances_tested += len(f)
        n_max = max(n_max, n)

    mean_comm_complexity = total_comm_complexity / instances_tested

    # Check if the mean communication complexity is within ±10% of O(n^2)
    conjecture_holds = abs(mean_comm_complexity - n_max**2) <= 0.1 * n_max**2
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "communication_complexity",
        "metric_value": mean_comm_complexity,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_comm_complexity = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_comm_complexity} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_comm_complexity} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")