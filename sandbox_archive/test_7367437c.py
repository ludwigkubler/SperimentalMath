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
    
    def generate_boolean_formula(n):
        return ''.join(random.choice('01') for _ in range(2**n - 1))
    
    def entropy(s):
        counts = [s.count(c) for c in '01']
        total = sum(counts)
        if total == 0:
            return 0
        p0, p1 = counts[0] / total, counts[1] / total
        return -p0 * math.log2(p0) - p1 * math.log2(p1)
    
    def k_theory_order(n):
        # Simplified approximation for demonstration purposes
        return n
    
    results = []
    instances_tested = 0
    n_max = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        formula = generate_boolean_formula(n)
        entropy_value = entropy(formula)
        order = k_theory_order(n)
        results.append((order, log_n_times_entropy))
        instances_tested += 1
        n_max = max(n_max, n)
    
    if not results:
        return {
            "metric_name": "k_theory_order",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "no_results"
        }
    
    log_n_times_entropy = [math.log(n) * entropy for n, _ in results]
    correlation_coefficient = sum(x*y for x, y in zip(results, log_n_times_entropy)) / len(results)
    
    return {
        "metric_name": "k_theory_order",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": 0.8 <= correlation_coefficient < 1.5,
        "counterexample": "" if 0.8 <= correlation_coefficient < 1.5 else "correlation_out_of_range"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 10**9) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["metric_value"] is not None for result in results):
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"correlation_out_of_range\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE some_trials_missing_data")