# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(10 * n):  # Ensure enough clauses to cover all variables
            clause = [random.choice([f'x{i}', f'-x{i}']) for i in range(1, n + 1)]
            random.shuffle(clause)
            clauses.append(' '.join(clause))
        return ' '.join(clauses)

    def circuit_monotone_width(cnf):
        # Simplified heuristic to estimate circuit monotone width
        return len(cnf.split())

    def minimal_noncommutative_tensor_power(cnf):
        # Simplified heuristic to estimate noncommutative tensor power
        return len(cnf.split()) ** 2

    n_values = [5, 10, 15, 20, 30, 40]
    metric_values = []
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):  # Ensure enough instances per size
            cnf = generate_cnf(n)
            w_phi = circuit_monotone_width(cnf)
            tensor_power = minimal_noncommutative_tensor_power(cnf)
            metric_values.append(tensor_power / w_phi)
            instances_tested += 1
            n_max = max(n_max, n)

    if len(metric_values) < 30:
        return {
            "metric_name": "minimal_noncommutative_tensor_power_over_w_phi",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }

    mean = sum(metric_values) / len(metric_values)
    std_dev = (sum((x - mean) ** 2 for x in metric_values) / len(metric_values)) ** 0.5

    return {
        "metric_name": "minimal_noncommutative_tensor_power_over_w_phi",
        "metric_value": mean,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": all(x <= y for x, y in zip(metric_values, [mean] * len(metric_values))),
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]  # Default to first 10 primes

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r['metric_value'] for r in results if r['metric_value'] is not None) / len(results)
    std_dev_metric_value = (sum((r['metric_value'] - mean_metric_value) ** 2 for r in results if r['metric_value'] is not None) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)

    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev_metric_value} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"not_supported\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")