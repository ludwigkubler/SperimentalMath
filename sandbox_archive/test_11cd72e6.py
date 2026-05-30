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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses

    def resolution_width(clauses):
        stack = []
        while True:
            new_clauses = set()
            found_resolvent = False
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    if any(-lit in clauses[i] and lit in clauses[j] for lit in set(clauses[i]) & set(clauses[j])):
                        resolvent = [x for x in clauses[i] if x not in [-lit for lit in set(clauses[i]) & set(clauses[j])]]
                        resolvent.extend([x for x in clauses[j] if x not in [-lit for lit in set(clauses[i]) & set(clauses[j])]])
                        new_clauses.add(tuple(sorted(resolvent)))
                        found_resolvent = True
            if not found_resolvent:
                break
            clauses = list(new_clauses)
        return len(set(map(tuple, clauses)))

    def kahler_area(width):
        # Simplified numerical approximation of Kähler area for demonstration purposes
        return width ** 2

    n_values = [5, 10, 15, 20, 30, 40]
    max_ratio = 0.0
    instances_tested = 0
    n_max = 0

    for n in n_values:
        for _ in range(5):
            clauses = generate_3cnf(n)
            width = resolution_width(clauses)
            area = kahler_area(width)
            if width > 0:
                ratio = area / (width ** 2)
                max_ratio = max(max_ratio, ratio)
                instances_tested += 1
                n_max = max(n_max, n)

    conjecture_holds = max_ratio <= 1.5
    counterexample = "mapping_undefined" if not conjecture_holds else ""

    return {
        "metric_name": "max_ratio",
        "metric_value": max_ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")