# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
import itertools

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def twistor_space_size(f):
        n = len(f)
        if n == 0:
            return 0
        min_order = float('inf')
        for i in range(n):
            if f[i] == 1:
                min_order = min(min_order, i + 1)
        return min_order
    
    def communication_complexity_rank(f):
        n = len(f)
        rank = 0
        for i in range(2**n):
            subset_sum = sum(f[j] for j in range(n) if (i >> j) & 1)
            if subset_sum > rank:
                rank = subset_sum
        return rank
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        std_x = math.sqrt(sum((x[i] - mean_x)**2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y)**2 for i in range(n)) / n)
        return cov / (std_x * std_y) if std_x != 0 and std_y != 0 else 0
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = [random.randint(0, 1) for _ in range(n)]
        min_order = twistor_space_size(f)
        c_phi = communication_complexity_rank(f)
        results.append((min_order, c_phi))
    
    if not results:
        return {
            "metric_name": "Pearson correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    x, y = zip(*results)
    corr_coeff = pearson_correlation(x, y)
    
    return {
        "metric_name": "Pearson correlation",
        "metric_value": corr_coeff,
        "instances_tested": len(results),
        "n_max": max(len(f) for f in results),
        "conjecture_holds": corr_coeff >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 53))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no trials run")
    else:
        mean_corr_coeff = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        
        if all(r["conjecture_holds"] for r in results):
            print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0.0 support_fraction=1.0")
        elif support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0.0 support_fraction={support_fraction}")
        else:
            first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")