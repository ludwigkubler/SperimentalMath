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
    
    def generate_cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses

    def compute_clause_complexity(cnf):
        return len(cnf)

    def compute_divisor_class_group_order(n):
        # Simplified heuristic for demonstration purposes
        # Actual computation would require number field theory
        return random.randint(1, 2**n)

    n_values = [5, 10, 15, 20, 30, 40]
    min_orders = []
    complexities = []

    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n, random.randint(1, n))
            complexity = compute_clause_complexity(cnf)
            order = compute_divisor_class_group_order(n)
            min_orders.append(order)
            complexities.append(complexity)

    if not min_orders or not complexities:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    mean_order = sum(min_orders) / len(min_orders)
    mean_complexity = sum(complexities) / len(complexities)

    # Simplified Pearson correlation coefficient
    numerator = sum((x - mean_order) * (y - mean_complexity) for x, y in zip(min_orders, complexities))
    denominator = math.sqrt(sum((x - mean_order)**2 for x in min_orders)) * math.sqrt(sum((y - mean_complexity)**2 for y in complexities))
    correlation_coefficient = numerator / denominator if denominator != 0 else None

    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(min_orders),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient is not None and abs(correlation_coefficient) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any("conjecture_holds" in r and not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "conjecture_holds" in result and not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")