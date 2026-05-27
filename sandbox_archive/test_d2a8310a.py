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
    
    def generate_sat_instance(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_minimal_rank(instance):
        # Placeholder function to compute minimal rank
        # This is a dummy implementation and should be replaced with actual algorithm
        return len(instance) // 2
    
    def solve_sat_instance(instance):
        # Placeholder function to solve SAT instance using exponential time algorithm
        # This is a dummy implementation and should be replaced with actual algorithm
        return random.choice([True, False])
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instance = generate_sat_instance(n)
        R_F = compute_minimal_rank(instance)
        solved = solve_sat_instance(instance)
        
        if not solved:
            counterexample = f"Instance of size {n} could not be solved"
            return {
                "metric_name": "R_F / (n * log^2(n))",
                "metric_value": None,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": counterexample
            }
        
        metric_value = R_F / (n * math.log(n) ** 2)
        results.append(metric_value)
    
    mean_metric_value = sum(results) / len(results)
    std_metric_value = math.sqrt(sum((x - mean_metric_value) ** 2 for x in results) / len(results))
    
    support_fraction = sum(1 for v in results if v <= 5) / len(results)
    
    return {
        "metric_name": "R_F / (n * log^2(n))",
        "metric_value": mean_metric_value,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.96,  # 5% margin of error
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='not supported by all seeds' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")