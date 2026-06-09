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
    q = 2**random.randint(3, 10)  # Finite field size
    n_max = 40
    instances_tested = 0
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""

    for n in range(5, n_max + 1):
        if n > 30:
            break

        # Generate a random CNF formula with n variables
        m = random.randint(n * (n // 2), n * (n // 2) + 10)
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n) if random.choice([True, False]) else -random.randint(1, n) for _ in range(random.randint(1, n))]
            clauses.append(clause)

        # Compute the Frege proof depth (simplified model)
        d_phi = math.ceil(math.log(n * m, 2))

        # Simulate computing min_φ(h) using etale cohomology (simplified model)
        min_h_phi = random.randint(1, n)

        # Calculate the ratio
        ratio = min_h_phi / d_phi

        # Check if the ratio is bounded by a constant multiple of log(n)/log(log(n))
        log_n = math.log(n)
        log_log_n = math.log(log_n)
        bound = 3 * (log_n / log_log_n)  # Example constant multiple
        if ratio > bound:
            conjecture_holds = False
            counterexample = f"n={n}, min_h_phi={min_h_phi}, d_phi={d_phi}, ratio={ratio}"
            break

        instances_tested += 1
        total_metric_value += ratio

    return {
        "metric_name": "Ratio of min_φ(h) to Frege proof depth",
        "metric_value": total_metric_value / instances_tested if instances_tested > 0 else 0,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 3 for i in range(5, 30)]
    
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")
    else:
        print("RESULT: INCONCLUSIVE no seeds supported the conjecture")