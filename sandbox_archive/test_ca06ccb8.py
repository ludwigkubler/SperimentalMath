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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity(f):
        n = int(math.log2(len(f)))
        if n == 0:
            return 0
        count = sum(1 for i in range(2**n) if f[i] != f[i ^ (1 << (n - 1))])
        return count / (2**(n - 1))
    
    def minimal_representation_length(f):
        n = int(math.log2(len(f)))
        if n == 0:
            return 0
        # Simplified Brauer group representation length for demonstration
        return n
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_boolean_function(n)
        comm_complexity = communication_complexity(f)
        br_len = minimal_representation_length(f)
        if br_len == 0:
            continue
        results.append(comm_complexity / br_len)
    
    if not results:
        return {
            "metric_name": "Comm(br_len)",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(0.5 <= x <= 2 for x in results) / len(results)
    
    return {
        "metric_name": "Comm(br_len)",
        "metric_value": mean,
        "instances_tested": len(results),
        "n_max": max(n for _ in range(30)),
        "conjecture_holds": support_fraction >= 0.9,
        "counterexample": "" if support_fraction >= 0.9 else f"support_fraction={support_fraction}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_dev_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and any(result["support_fraction"] >= 0.9 for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"support_fraction={result['support_fraction']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")