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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank(phi):
        # Placeholder function; actual implementation needed
        return len(phi)
    
    def minimal_order_eigenform(k):
        # Placeholder function; actual implementation needed
        return k
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_correlation = 0
    max_n = 0
    
    for n in n_values:
        for _ in range(5):  # Sample 5 instances per size
            phi = generate_boolean_function(n)
            r_phi = communication_complexity_rank(phi)
            order_k = minimal_order_eigenform(r_phi)
            instances_tested += 1
            max_n = max(max_n, n)
            
            if r_phi == 0:
                continue
            
            correlation = abs(order_k - r_phi) / (r_phi * order_k)
            total_correlation += correlation
    
    mean_correlation = total_correlation / instances_tested
    conjecture_holds = mean_correlation >= 0.5
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "mean_absolute_difference",
        "metric_value": mean_correlation,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")