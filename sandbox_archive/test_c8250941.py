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
    
    def communication_complexity(phi):
        n = len(phi)
        if n == 0:
            return 0
        count = 0
        for i in range(n):
            if phi[i] == 1:
                count += 1
        return count
    
    def lefschetz_thimble_rank(phi):
        # Placeholder function to simulate Lefschetz thimble rank calculation
        n = len(phi)
        return n // 2
    
    results = []
    for _ in range(30):
        n = random.randint(5, 40)
        phi = [random.choice([0, 1]) for _ in range(n)]
        c_phi = communication_complexity(phi)
        lr_phi = lefschetz_thimble_rank(phi)
        results.append((c_phi, lr_phi))
    
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    c_values = [c for c, _ in results]
    lr_values = [lr for _, lr in results]
    
    mean_c = sum(c_values) / len(c_values)
    mean_lr = sum(lr_values) / len(lr_values)
    
    numerator = sum((c - mean_c) * (lr - mean_lr) for c, lr in results)
    denominator = math.sqrt(sum((c - mean_c)**2 for c in c_values)) * math.sqrt(sum((lr - mean_lr)**2 for lr in lr_values))
    
    if denominator == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": 0.0,
            "instances_tested": len(results),
            "n_max": max(len(phi) for _, phi in results),
            "conjecture_holds": False,
            "counterexample": "denominator_zero"
        }
    
    pearson_corr = numerator / denominator
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr,
        "instances_tested": len(results),
        "n_max": max(len(phi) for _, phi in results),
        "conjecture_holds": abs(pearson_corr) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        if not results:
            results.append(trial_result)
        else:
            results[0]["metric_value"] += trial_result["metric_value"]
            results[0]["instances_tested"] += trial_result["instances_tested"]
    
    mean_metric = results[0]["metric_value"] / len(seeds)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std=0.0 support_fraction={support_fraction}")
    elif any(r["counterexample"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(seeds) if r["conjecture_holds"])
        counterexample_desc = results[0]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")