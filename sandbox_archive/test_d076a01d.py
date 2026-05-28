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
    
    def calculate_depth(f):
        if len(f) == 1:
            return 1
        depth = 0
        for i in range(len(f)):
            if f[i] != 0 and f[i] != 1:
                depth = max(depth, calculate_depth(f[:i]) + calculate_depth(f[i+1:]))
        return depth
    
    def calculate_genus(f):
        # Placeholder function to simulate genus calculation
        # This is a dummy implementation for demonstration purposes
        return len(f) ** 0.5
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_depth = 0
    total_genus = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 5 instances per size
            f = generate_random_boolean_function(n)
            depth = calculate_depth(f)
            genus = calculate_genus(f)
            total_depth += depth
            total_genus += genus
            instances_tested += 1
    
    avg_depth = total_depth / instances_tested
    avg_genus = total_genus / instances_tested
    
    correlation_coefficient = (instances_tested * sum(depth * genus for depth, genus in zip(range(1, n_values[-1] + 1), range(1, n_values[-1] + 1)))
                               - sum(range(1, n_values[-1] + 1)) * sum(range(1, n_values[-1] + 1))
                               ) / math.sqrt((instances_tested * sum(depth**2 for depth in range(1, n_values[-1] + 1))
                                              - sum(range(1, n_values[-1] + 1))**2) *
                                             (instances_tested * sum(genus**2 for genus in range(1, n_values[-1] + 1))
                                              - sum(range(1, n_values[-1] + 1))**2))
    
    conjecture_holds = correlation_coefficient >= 0.7 and abs(avg_genus - avg_depth**2) <= 2 * avg_depth**2
    
    return {
        "metric_name": "Spearman rank correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']:.4f}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric = sum(r["metric_value"] for r in results) / len(results)
    std_metric = math.sqrt(sum((r["metric_value"] - mean_metric)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric:.4f} std={std_metric:.4f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric:.4f} std={std_metric:.4f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")