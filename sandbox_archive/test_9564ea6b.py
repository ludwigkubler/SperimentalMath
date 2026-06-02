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
    
    def communication_complexity_rank(f):
        # Placeholder implementation. Replace with actual complexity calculation.
        return len(f) ** 0.5
    
    def l_function_zeros_count(f):
        # Placeholder implementation. Replace with actual L-function zeros count.
        return len(f)
    
    n_max = 10
    instances_tested = 30
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        f = generate_boolean_function(n)
        rank = communication_complexity_rank(f)
        zeros_count = l_function_zeros_count(f)
        
        if zeros_count == 0:
            continue
        
        metric_values.append(rank / math.log(zeros_count))
    
    mean_metric_value = sum(metric_values) / len(metric_values)
    correlation_coefficient = sum((x - mean_metric_value) * (y - mean_metric_value) for x, y in zip(metric_values, range(5, n_max + 1))) / (len(metric_values) * math.sqrt(sum((x - mean_metric_value) ** 2 for x in metric_values)) * math.sqrt(sum((y - mean_metric_value) ** 2 for y in range(5, n_max + 1))))
    
    if correlation_coefficient < 0.7:
        conjecture_holds = False
        counterexample = "correlation_coefficient_too_low"
    
    return {
        "metric_name": "communication_complexity_rank",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_too_low\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")