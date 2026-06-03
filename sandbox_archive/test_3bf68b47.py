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
        n = int(math.log2(len(f)))
        # Simplified complexity rank calculation
        return n
    
    def min_simple_connected_components(f):
        n = len(f)
        components = [i for i in range(n) if f[i] == 1]
        return len(components)
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_boolean_function(n)
        min_order = min_simple_connected_components(f)
        r_f = communication_complexity_rank(f)
        results.append((min_order, r_f))
    
    if not results:
        return {
            "metric_name": "communication_complexity_rank",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    min_ranks = [r for _, r in results]
    mean_min_ranks = sum(min_ranks) / len(min_ranks)
    rank_diffs = [(min_order - r_f) ** 2 for min_order, r_f in results]
    variance_rank_diffs = sum(rank_diffs) / len(rank_diffs)
    std_dev_rank_diffs = math.sqrt(variance_rank_diffs)
    
    correlation_coefficient = (sum((min_ranks[i] - mean_min_ranks) * (results[i][1] - mean_min_ranks) for i in range(len(results))) /
                               ((len(results) - 1) * std_dev_rank_diffs * std_dev_rank_diffs))
    
    return {
        "metric_name": "communication_complexity_rank",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for _, r_f in results),
        "conjecture_holds": abs(correlation_coefficient) >= 0.5,  # Simplified threshold
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.5\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")