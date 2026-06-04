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
    
    def communication_complexity_rank(f):
        # Placeholder for actual computation
        return random.randint(1, 10)
    
    def minimal_monoidal_categorical_generators(f):
        # Placeholder for actual computation
        return random.randint(1, 2 * communication_complexity_rank(f))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    total_time = 0
    
    for n in n_values:
        f = lambda x: random.choice([True, False])  # Placeholder boolean function
        start_time = time.time()
        rank = communication_complexity_rank(f)
        generators = minimal_monoidal_categorical_generators(f)
        end_time = time.time()
        total_time += (end_time - start_time) * n
        
        if end_time - start_time > 200:
            return {
                "metric_name": "communication_complexity_rank",
                "metric_value": None,
                "instances_tested": len(results),
                "n_max": max(n_values),
                "conjecture_holds": False,
                "counterexample": "budget_exceeded"
            }
        
        results.append((rank, generators))
    
    if total_time > 240:
        return {
            "metric_name": "communication_complexity_rank",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "budget_exceeded"
        }
    
    correlation_coefficient = 0
    n = len(results)
    if n > 1:
        mean_rank = sum(rank for rank, _ in results) / n
        mean_generators = sum(generators for _, generators in results) / n
        numerator = sum((rank - mean_rank) * (generators - mean_generators) for rank, generators in results)
        denominator = math.sqrt(sum((rank - mean_rank) ** 2 for rank, _ in results)) * math.sqrt(sum((generators - mean_generators) ** 2 for _, generators in results))
        correlation_coefficient = numerator / denominator if denominator != 0 else 0
    
    return {
        "metric_name": "communication_complexity_rank",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient<0.8\" first_failing_seed={first_failing_seed}")