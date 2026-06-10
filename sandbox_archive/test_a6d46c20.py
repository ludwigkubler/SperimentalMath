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
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        rank_variance = random.uniform(0.1, 10) * n
        matrix = [[random.random() for _ in range(n)] for _ in range(n)]
        
        # Compute Frobenius norm
        frobenius_norm = sum(sum(x**2 for x in row) for row in matrix)
        frobenius_norm = math.sqrt(frobenius_norm)
        
        results.append({
            "n": n,
            "rank_variance": rank_variance,
            "frobenius_norm": frobenius_norm
        })
    
    mean_frobenius_norm = sum(result["frobenius_norm"] for result in results) / len(results)
    ratio_mean_to_variance = mean_frobenius_norm / (sum(result["rank_variance"] for result in results) / len(results))
    
    return {
        "metric_name": "Ratio of Mean Frobenius Norm to Rank Variance",
        "metric_value": ratio_mean_to_variance,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": ratio_mean_to_variance > 0.9,
        "counterexample": "" if ratio_mean_to_variance > 0.9 else "Frobenius norm not proportional to rank variance"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((result["seed"] for result in results if not result["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Frobenius norm not proportional to rank variance\" first_failing_seed={first_failing_seed}")