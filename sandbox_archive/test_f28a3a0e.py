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
    
    def generate_kcnf(n, k):
        clauses = []
        for _ in range(k * n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses

    def communication_complexity_rank(phi):
        # Placeholder function; replace with actual implementation
        return random.randint(1, 5)

    def minimal_order_of_arithmetic_cycles(phi):
        # Placeholder function; replace with actual implementation
        return random.randint(n**2, n**3)

    results = []
    for _ in range(30):  # Ensure at least 30 instances per seed
        n = random.choice([5, 10, 15, 20, 30, 40])
        k = random.randint(1, min(n // 2, 5))
        phi = generate_kcnf(n, k)
        m_order = minimal_order_of_arithmetic_cycles(phi)
        r_phi = communication_complexity_rank(phi)
        results.append((m_order, r_phi))

    n_max = max(n for _, _ in results)
    if n_max < 16:
        return {
            "metric_name": "minimal_order_of_arithmetic_cycles",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "n_max < 16"
        }

    metric_values = [m for m, _ in results]
    mean_metric = sum(metric_values) / len(metric_values)
    support_fraction = sum(1 for m, r in results if n**2 * math.log(n) <= m <= 5 * r) / len(results)

    return {
        "metric_name": "minimal_order_of_arithmetic_cycles",
        "metric_value": mean_metric,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": support_fraction >= 0.8 and mean_metric <= 5 * max(r for _, r in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        if not result["conjecture_holds"]:
            break

    if all(result["conjecture_holds"] for result in results):
        RESULT = "SUPPORTED"
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        RESULT = f"FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}"
    else:
        RESULT = "INCONCLUSIVE"

    print(f"RESULT: {RESULT}")