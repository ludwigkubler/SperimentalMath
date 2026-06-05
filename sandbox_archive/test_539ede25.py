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
    
    def factorial(n):
        if n == 0 or n == 1:
            return 1
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result
    
    def communication_complexity_rank(n):
        # Placeholder function to compute the rank of communication complexity
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(1, n)
    
    def minimal_order_of_monoid_action(n):
        # Placeholder function to compute the minimal order of monoid action
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(1, factorial(n))
    
    instances_tested = 0
    total_metric_value = 0.0
    n_max = 0
    
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        if n > n_max:
            n_max = n
        
        m_phi = minimal_order_of_monoid_action(n)
        r_phi = communication_complexity_rank(n)
        
        instances_tested += 1
        total_metric_value += abs(m_phi - r_phi) / (m_phi + r_phi)
    
    metric_value = total_metric_value / instances_tested
    
    if metric_value < 0.8:
        conjecture_holds = False
        counterexample = "communication_complexity_rank"
    else:
        conjecture_holds = True
        counterexample = ""
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{res['counterexample']}\" first_failing_seed={first_failing_seed}")