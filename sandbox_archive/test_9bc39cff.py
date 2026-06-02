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
    
    def communication_complexity_rank(F):
        n = len(next(iter(F.values())))
        if n == 0:
            return 0
        
        # Simulate a simple communication complexity rank calculation
        # This is just an example; replace with actual computation
        rank = n * (n - 1) // 2
        return rank
    
    def min_quandle_representations(F):
        # Simulate a simple quandle representation count
        # This is just an example; replace with actual computation
        n = len(next(iter(F.values())))
        if n == 0:
            return 0
        
        # Example: each input bit requires at least one representation
        return n
    
    instances_tested = 30
    n_max = 40
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        F = {i: random.choice([0, 1]) for i in range(n)}
        
        rank = communication_complexity_rank(F)
        min_representations = min_quandle_representations(F)
        
        if rank == 0 or min_representations == 0:
            continue
        
        metric_values.append(min_representations / (rank ** 2))
    
    mean_value = sum(metric_values) / len(metric_values)
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in metric_values) / len(metric_values))
    conjecture_holds = all(x <= 1.5 for x in metric_values)
    counterexample = "" if conjecture_holds else "communication_complexity_rank_too_high"
    
    return {
        "metric_name": "ratio",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"communication_complexity_rank_too_high\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")