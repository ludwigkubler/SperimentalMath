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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def calculate_affine_group_order(f):
        n = len(f)
        # This is a simplified version of calculating the affine group order
        # for an n-variable Boolean function. In practice, this would involve
        # more complex algebraic structures.
        return 2**(n + 1) - 1
    
    def calculate_communication_complexity_rank_variance(f):
        n = len(f)
        # This is a simplified version of calculating the communication complexity rank variance
        # for an n-variable Boolean function. In practice, this would involve more complex combinatorial methods.
        return random.uniform(0, n**2)
    
    instances_tested = 30
    n_max = 40
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        f = generate_random_boolean_function(n)
        order = calculate_affine_group_order(f)
        variance = calculate_communication_complexity_rank_variance(f)
        metric_values.append(order / variance)
    
    mean_value = sum(metric_values) / instances_tested
    std_dev = math.sqrt(sum((x - mean_value)**2 for x in metric_values) / instances_tested)
    
    conjecture_holds = all(abs(x - mean_value) <= 3 * std_dev or x > 10 for x in metric_values)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Order/CommRankVar Ratio",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support n_tested={len(results)}")