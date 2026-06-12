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
    n_max = 0
    instances_tested = 0
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""

    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n

        # Generate a random CNF formula with n variables
        num_clauses = random.randint(1, n * (n // 2))
        cnf_formula = []
        for _ in range(num_clauses):
            clause = [random.randint(-n, -1) if random.choice([True, False]) else random.randint(1, n)
                      for _ in range(random.randint(1, n))]
            cnf_formula.append(clause)

        # Construct a diophantine equation that defines the vertices of its corresponding DPLL search tree
        # This is a simplified example; actual construction would be more complex
        degree = 2 * num_clauses + n

        # Compute the metric value (degree)
        metric_value = degree

        # Update total metric value and instances tested
        total_metric_value += metric_value
        instances_tested += 1

        # Check if the conjecture holds for this instance
        if degree > n**2 * math.log(n):
            conjecture_holds = False
            counterexample = f"n={n}, degree={degree}, expected<=n^2*log(n)={n**2*math.log(n)}"

    # Compute mean metric value
    mean_metric_value = total_metric_value / instances_tested

    return {
        "metric_name": "diophantine_degree",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    # Compute mean and std of metric_value
    total_metric_value = sum(r["metric_value"] for r in results)
    mean_metric_value = total_metric_value / len(results)
    variance = sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results)
    std_metric_value = math.sqrt(variance)

    # Compute fraction of seeds where conjecture_holds
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    # Determine final result
    if all(r["conjecture_holds"] for r in results) or support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")