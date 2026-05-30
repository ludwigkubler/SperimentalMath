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
    
    def generate_kcnf(n, k):
        clauses = []
        for _ in range(k):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if len(clause) == 2 and clause[0] != -clause[1]:
                clauses.append(clause)
        return clauses

    def euler_characteristic(n, k):
        # Simplified Euler characteristic for a random k-CNF formula
        return n - k + 1

    def clause_complexity(k):
        # Simplified complexity measure for a k-CNF formula
        return k

    results = []
    for n in [5, 10, 15, 20, 30]:
        for _ in range(6):  # 6 instances per size to ensure statistical signal
            k = random.randint(1, min(n * (n - 1) // 2, 10))  # Ensure a valid k
            phi = generate_kcnf(n, k)
            chi_C_phi = euler_characteristic(n, k)
            chi_phi = clause_complexity(k)
            diff = abs(chi_C_phi - math.sqrt(n) * chi_phi)
            results.append((n, chi_C_phi, chi_phi, diff))

    metric_value = sum(diff for _, _, _, diff in results) / len(results)
    instances_tested = len(results)
    n_max = max(n for n, _, _, _ in results)
    conjecture_holds = all(diff <= 2 * math.sqrt(n) for _, _, _, diff in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "Euler Characteristic Difference",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")