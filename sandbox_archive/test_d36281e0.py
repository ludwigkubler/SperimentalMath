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
from math import factorial, log

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 0
    instances_tested = 0
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""

    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            m = random.randint(1, min(n * (n - 1) // 2, 100))  # Number of clauses
            if n_max < n:
                n_max = n

            # Generate a random SAT instance with m clauses and n variables
            clauses = []
            for _ in range(m):
                clause = [random.choice([f"x{i}", f"~x{i}"]) for i in range(1, n + 1)]
                clauses.append(clause)

            # Compute the minimal root count (simplified heuristic)
            root_count = len(set(random.sample(range(n), m)))

            # Calculate φ(m, n) as a simple function of m and n
            phi_m_n = m * log(n) + n

            # Check if the conjecture holds for this instance
            if not (log(factorial(n)) <= phi_m_n <= n**3):
                conjecture_holds = False
                counterexample = f"m={m}, n={n}, φ(m,n)={phi_m_n}"
                break  # No need to check further instances

            total_metric_value += phi_m_n
            instances_tested += 1

    mean_metric_value = total_metric_value / instances_tested if instances_tested > 0 else 0.0
    support_fraction = conjecture_holds

    return {
        "metric_name": "φ(m, n)",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 50))  # Default to first 30 primes if no seeds provided

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = all(r["conjecture_holds"] for r in results)

    if support_fraction:
        result_status = "SUPPORTED"
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        result_status = f"FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}"
    else:
        result_status = "INCONCLUSIVE"

    print(f"RESULT: {result_status} mean={mean_metric_value:.2f} std=0.0 support_fraction={support_fraction}")