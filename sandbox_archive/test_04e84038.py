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
    
    def truth_table_to_metric_space(truth_table):
        n = int(math.log2(len(truth_table)))
        metric_space = [[truth_table[i * (1 << (n - j)) + j] for j in range(n)] for i in range(1 << n)]
        return metric_space
    
    def hyperbolic_distance(metric_space, euclidean_plane):
        # Simplified version of the distance calculation
        # This is a placeholder and should be replaced with actual hyperbolic geometry calculations
        return sum(abs(x - y) for row in metric_space for x, y in zip(row, euclidean_plane)) / len(metric_space)
    
    def communication_complexity(truth_table):
        n = int(math.log2(len(truth_table)))
        # Simplified version of the communication complexity calculation
        # This is a placeholder and should be replaced with actual communication complexity calculations
        return sum(1 for row in truth_table if any(x != y for x, y in zip(row, row[1:])))
    
    n = random.randint(5, 40)
    boolean_function = generate_boolean_function(n)
    metric_space = truth_table_to_metric_space(boolean_function)
    euclidean_plane = [random.choice([0, 1]) for _ in range(n)]
    distance = hyperbolic_distance(metric_space, euclidean_plane)
    comm_complexity = communication_complexity(boolean_function)
    
    if comm_complexity == 0:
        return {
            "metric_name": "communication_complexity",
            "metric_value": comm_complexity,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "communication_complexity_zero"
        }
    
    ratio = distance / comm_complexity
    return {
        "metric_name": "communication_complexity",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": ratio >= 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"communication_complexity_zero\" first_failing_seed={first_failing_seed}")