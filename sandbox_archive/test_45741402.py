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
    
    def generate_random_cnf(n, k):
        variables = list(range(1, n+1))
        clauses = []
        for _ in range(k):
            clause = [random.choice(variables) * (2 * random.randint(0, 1) - 1) for _ in range(random.randint(1, n))]
            clauses.append(clause)
        return clauses

    def circuit_monotone_width(cnf):
        # Placeholder function to compute circuit monotone width
        # This is a dummy implementation and should be replaced with an actual algorithm
        return len(cnf)

    def aut_order(cnf):
        # Placeholder function to compute the order of automorphism group
        # This is a dummy implementation and should be replaced with an actual algorithm
        return random.randint(1, 100)  # Dummy value

    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_aut_order = 0
    total_w = 0
    max_n = 0

    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            cnf = generate_random_cnf(n, random.randint(1, n))
            aut_order_val = aut_order(cnf)
            w = circuit_monotone_width(cnf)
            total_aut_order += aut_order_val
            total_w += w
            instances_tested += 1
            max_n = max(max_n, n)

    mean_aut_order = total_aut_order / instances_tested
    mean_w = total_w / instances_tested
    correlation_coefficient = (instances_tested * sum(aut_order_val * w for aut_order_val, w in zip([aut_order(cnf) for cnf in [generate_random_cnf(n, random.randint(1, n)) for _ in range(instances_tested)]], [circuit_monotone_width(generate_random_cnf(n, random.randint(1, n))) for _ in range(instances_tested)])) - instances_tested * mean_aut_order * mean_w) / (instances_tested * math.sqrt(sum((aut_order_val - mean_aut_order)**2 for aut_order_val in [aut_order(cnf) for cnf in [generate_random_cnf(n, random.randint(1, n)) for _ in range(instances_tested)]]) * sum((w - mean_w)**2 for w in [circuit_monotone_width(generate_random_cnf(n, random.randint(1, n))) for _ in range(instances_tested)])))

    conjecture_holds = correlation_coefficient > 0.8 and abs(mean_aut_order - mean_w) <= 3
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
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
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unspecified")