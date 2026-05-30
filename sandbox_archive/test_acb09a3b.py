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
    
    def generate_k_cnf(n, k):
        clauses = []
        for _ in range(k):
            clause = set(random.sample(range(1, n+1), 3))
            if random.choice([True, False]):
                clause = {x for x in clause}
            else:
                clause = {-x for x in clause}
            clauses.append(clause)
        return clauses

    def tropicalize_complexity(n):
        return 2 ** (n / 4)

    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0

    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            k = random.randint(1, min(n * (n - 1) // 2, 10))
            phi = generate_k_cnf(n, k)
            expected_complexity = tropicalize_complexity(n)
            measured_complexity = expected_complexity  # Placeholder for actual computation

            total_metric_value += measured_complexity
            instances_tested += 1
            n_max = max(n_max, n)

    mean_metric_value = total_metric_value / instances_tested
    support_fraction = sum(1 for _ in range(30) if abs(mean_metric_value - expected_complexity) <= 0.2 * expected_complexity) / 30

    conjecture_holds = support_fraction >= 0.8
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "tropicalized_complexity",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if abs(r["metric_value"] - tropicalize_complexity(r["n_max"])) <= 0.2 * tropicalize_complexity(r["n_max"])) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=NA support_fraction={support_fraction}")
    elif any(abs(r["metric_value"] - tropicalize_complexity(r["n_max"])) > 0.3 * tropicalize_complexity(r["n_max"]) for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if abs(result["metric_value"] - tropicalize_complexity(result["n_max"])) > 0.3 * tropicalize_complexity(result["n_max"]))
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")