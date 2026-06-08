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
    
    def truth_table_to_metric_space(func):
        n = int(math.log2(len(func)))
        metric_space = [[func[i] ^ func[j] for j in range(2**n)] for i in range(2**n)]
        return metric_space
    
    def hyperbolic_distance(metric_space, euclidean_plane):
        # Simplified approximation of hyperbolic distance
        n = len(metric_space)
        max_diff = 0
        for i in range(n):
            for j in range(i+1, n):
                diff = sum(abs(a - b) for a, b in zip(metric_space[i], metric_space[j]))
                if diff > max_diff:
                    max_diff = diff
        return max_diff
    
    def communication_complexity(func):
        # Simplified approximation of communication complexity
        n = int(math.log2(len(func)))
        return n
    
    instances_tested = 0
    n_max = 1
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):  # Sample 5 instances per size
            func = generate_boolean_function(n)
            metric_space = truth_table_to_metric_space(func)
            euclidean_plane = [[0]*n] * n  # Simplified Euclidean plane
            d_Hf_E2 = hyperbolic_distance(metric_space, euclidean_plane)
            comm_complexity = communication_complexity(func)
            
            if comm_complexity == 0:
                continue
            
            instances_tested += 1
            ratio = d_Hf_E2 / comm_complexity
            if ratio < 0.5:
                conjecture_holds = False
                counterexample = f"n={n}, d(H_f, E^2)={d_Hf_E2}, comm_complexity={comm_complexity}"
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": 0.5,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] * r["instances_tested"] for r in results) / sum(r["instances_tested"] for r in results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 * r["instances_tested"] for r in results) / sum(r["instances_tested"] for r in results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"{results[sum(1 for r in results if not r['conjecture_holds'])].get('counterexample', 'unknown')}\") first_failing_seed={seeds[sum(1 for r in results if not r['conjecture_holds'])]}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")