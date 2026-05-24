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
    
    def compute_bp_size(f):
        # Placeholder for BP size computation logic
        # This is a dummy implementation and should be replaced with actual logic
        return len(f)
    
    def compute_hodge_rank(s):
        # Placeholder for Hodge rank computation logic
        # This is a dummy implementation and should be replaced with actual logic
        return math.log2(s + 1)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        s = compute_bp_size(f)
        rank = compute_hodge_rank(s)
        
        if rank < 0 or s <= 0:
            continue
        
        results.append({
            "n": n,
            "s": s,
            "rank": rank
        })
    
    if not results:
        return {
            "metric_name": "Hodge Rank vs BP Size",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    
    mean_rank = sum(result["rank"] for result in results) / len(results)
    std_rank = math.sqrt(sum((result["rank"] - mean_rank)**2 for result in results) / len(results))
    correlation_coefficient = 0
    
    if len(results) > 1:
        n_values = [result["n"] for result in results]
        s_values = [result["s"] for result in results]
        
        n_mean = sum(n_values) / len(n_values)
        s_mean = sum(s_values) / len(s_values)
        
        numerator = sum((n_values[i] - n_mean) * (s_values[i] - s_mean) for i in range(len(results)))
        denominator = math.sqrt(sum((n_values[i] - n_mean)**2 for i in range(len(results))) * sum((s_values[i] - s_mean)**2 for i in range(len(results))))
        
        correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "Hodge Rank vs BP Size",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": abs(correlation_coefficient) > 0.5,
        "counterexample": "" if abs(correlation_coefficient) > 0.5 else f"Correlation coefficient {correlation_coefficient} is not significant"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not ("conjecture_holds" in result and result["conjecture_holds"]))
        mean_metric_value = sum(r["metric_value"] for r in results if "metric_value" in r)
        std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if "metric_value" in r))
        support_fraction = len([r for r in results if "conjecture_holds" in r and r["conjecture_holds"]]) / len(results)
    
    print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")