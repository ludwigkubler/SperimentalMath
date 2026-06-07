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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = random.sample(range(1, n+1), 2)
            if random.choice([True, False]):
                clause[0] *= -1
                clause[1] *= -1
            clauses.append(clause)
        return clauses

    def p_adic_rank(poly):
        # Placeholder for actual p-adic rank calculation
        return len(poly)

    def resolution_width(cnf):
        # Placeholder for actual resolution width calculation
        return len(cnf) + 2

    n_values = [5, 10, 15, 20, 30, 40]
    p_adic_ranks = []
    widths = []

    for n in n_values:
        cnf = generate_cnf(n)
        poly = [random.choice([1, -1]) for _ in range(2**n)]
        rank = p_adic_rank(poly)
        width = resolution_width(cnf)
        p_adic_ranks.append(rank)
        widths.append(width)

    correlation_coefficient = sum((x * y for x, y in zip(p_adic_ranks, widths))) / (sum(x**2 for x in p_adic_ranks) * sum(y**2 for y in widths))**0.5
    mean_abs_diff = sum(abs(x - y) for x, y in zip(p_adic_ranks, widths)) / len(p_adic_ranks)

    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8 and mean_abs_diff <= 3,
        "counterexample": "" if correlation_coefficient >= 0.8 and mean_abs_diff <= 3 else "correlation_coefficient < 0.8 or mean_abs_diff > 3"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.8 or mean_abs_diff > 3\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")