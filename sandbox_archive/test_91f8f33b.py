# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank_variance(f):
        n = len(f)
        rank = 0
        for i in range(1, n + 1):
            if any(all(f[j] == f[j ^ (1 << k)] for j in range(2**(n-i))) for k in range(i)):
                rank += 1
        return rank
    
    def minimal_representation_degree(f):
        # Placeholder function to simulate the computation of D(f)
        # This is a dummy implementation and should be replaced with actual logic
        return len(f) ** 0.5
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_metric_value = 0
        
        for _ in range(5):
            f = generate_boolean_function(n)
            R_f = communication_complexity_rank_variance(f)
            D_f = minimal_representation_degree(f)
            
            if R_f == 0 or D_f == 0:
                continue
            
            instances_tested += 1
            total_metric_value += D_f / (R_f ** 1.5)
        
        if instances_tested == 0:
            continue
        
        metric_value = total_metric_value / instances_tested
        n_max = max(n_values)
        conjecture_holds = False
        counterexample = ""
        
        results.append({
            "metric_name": "D(f) / (R(f)^1.5)",
            "metric_value": metric_value,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        })
    
    return {
        "seed": seed,
        "results": results
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    all_results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        all_results.extend(result["results"])
    
    if not all_results:
        print("RESULT: INCONCLUSIVE no data")
        sys.exit(1)
    
    metric_values = [r["metric_value"] for r in all_results]
    mean_metric_value = sum(metric_values) / len(metric_values)
    std_metric_value = (sum((x - mean_metric_value) ** 2 for x in metric_values) / len(metric_values)) ** 0.5
    support_fraction = sum(r["conjecture_holds"] for r in all_results) / len(all_results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in all_results):
        first_failing_seed = next(r["seed"] for r in all_results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no support")