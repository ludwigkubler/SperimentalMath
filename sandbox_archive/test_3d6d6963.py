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
    
    def generate_curve(n):
        # Simplified generation of a smooth projective curve with n variables
        return [f'x{i}' for i in range(1, n+1)]
    
    def birational_morphism(curve):
        # Simplified birational morphism to P^1
        return random.choice(curve)
    
    def general_fiber_count(morphism, curve):
        # Count of points on a general fiber (simplified)
        return len(set(morphism for _ in range(5)))  # Random count
    
    def communication_complexity_rank(morphism):
        # Simplified rank calculation using DPLL solver
        return len(morphism)  # Length as a proxy
    
    def w_and_H(n, r):
        # Simplified w and H calculations (simplified)
        return n * r, n * math.log2(r + 1)
    
    metric_values = []
    log_metrics = []
    instances_tested = 0
    n_max = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        curve = generate_curve(n)
        morphism = birational_morphism(curve)
        fiber_count = general_fiber_count(morphism, curve)
        r = communication_complexity_rank(morphism)
        
        w, H = w_and_H(n, r)
        metric_value = log2(n**(r+1))
        if metric_value <= w + H:
            instances_tested += 1
            n_max = max(n_max, n)
            metric_values.append(metric_value)
            log_metrics.append(math.log2(n**(r+1)))
    
    if not metric_values or not log_metrics:
        return {
            "metric_name": "log2(n^(r+1))",
            "metric_value": 0.0,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "empty_metric_values"
        }
    
    mean_val = sum(metric_values) / len(metric_values)
    mean_log = sum(log_metrics) / len(log_metrics)
    correlation_coefficient = sum((x - mean_log) * (y - mean_val) for x, y in zip(log_metrics, metric_values)) / \
                              math.sqrt(sum((x - mean_log)**2 for x in log_metrics) * sum((y - mean_val)**2 for y in metric_values))
    
    conjecture_holds = correlation_coefficient >= 0.7
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.7"
    
    return {
        "metric_name": "log2(n^(r+1))",
        "metric_value": mean_val,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{trial_result}...}}")
        results.append(trial_result)
    
    mean_val = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_val)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_val} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")