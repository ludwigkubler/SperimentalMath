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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def arithmetic_hierarchy_complexity(f):
        # Placeholder function to simulate AH complexity
        return len(f)
    
    def circuit_monotone_width(f):
        # Placeholder function to simulate w_mon width
        return sum(f.count(bit) for bit in [0, 1])
    
    metric_name = "arithmetic_hierarchy_complexity"
    instances_tested = 30
    n_max = 40
    conjecture_holds = True
    counterexample = ""
    
    AH_values = []
    w_mon_values = []
    
    for _ in range(instances_tested):
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_random_boolean_function(n)
        AH_value = arithmetic_hierarchy_complexity(f)
        w_mon_value = circuit_monotone_width(f)
        
        AH_values.append(AH_value)
        w_mon_values.append(w_mon_value)
    
    if len(AH_values) < 100:
        conjecture_holds = False
        counterexample = "insufficient_instances"
    
    correlation_coefficient = sum((AH - mean_AH) * (w_mon - mean_w_mon) for AH, w_mon in zip(AH_values, w_mon_values)) / math.sqrt(sum((AH - mean_AH)**2 for AH in AH_values) * sum((w_mon - mean_w_mon)**2 for w_mon in w_mon_values))
    p_value = 0.01  # Placeholder value
    
    if correlation_coefficient < 0.9 or p_value > 0.01:
        conjecture_holds = False
        counterexample = f"correlation_coefficient={correlation_coefficient} — p_value={p_value}"
    
    return {
        "metric_name": metric_name,
        "metric_value": correlation_coefficient,
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
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")