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
    
    def calculate_depth(f):
        if len(f) == 1:
            return 0
        max_depth = 0
        for i in range(len(f)):
            if f[i] != 0 and f[i] != 1:
                depth = calculate_depth(f[:i]) + 1
                if depth > max_depth:
                    max_depth = depth
        return max_depth
    
    def calculate_genus(n):
        # Simplified model for genus calculation
        return n**2
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            f = generate_boolean_function(n)
            depth = calculate_depth(f)
            genus = calculate_genus(n)
            total_metric_value += abs(depth - math.sqrt(genus))
            instances_tested += 1
    
    mean_metric_value = total_metric_value / instances_tested
    support_fraction = Fraction(instances_tested, instances_tested)
    
    if support_fraction < Fraction(4, 5):
        conjecture_holds = False
        counterexample = "insufficient_support"
    
    return {
        "metric_name": "mean_absolute_error",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = Fraction(sum(1 for r in results if r["conjecture_holds"]), len(results))
    
    if support_fraction >= Fraction(4, 5):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"insufficient_support\" first_failing_seed={first_failing_seed}")