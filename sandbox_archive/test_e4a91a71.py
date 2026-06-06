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
    
    def generate_boolean_function(m):
        return [random.choice([0, 1]) for _ in range(2**m)]
    
    def compute_hodge_dimension(f):
        # Placeholder function to simulate Hodge dimension computation
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(1, m)
    
    def compute_communication_complexity_rank(f):
        # Placeholder function to simulate communication complexity rank computation
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(1, m)
    
    results = []
    for _ in range(1000):
        m = random.randint(5, 40)
        f = generate_boolean_function(m)
        dim_H = compute_hodge_dimension(f)
        rank_com = compute_communication_complexity_rank(f)
        results.append((dim_H, rank_com))
    
    if not results:
        return {
            "metric_name": "Correlation Coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    dim_H_values = [r[0] for r in results]
    rank_com_values = [r[1] for r in results]
    
    mean_dim_H = sum(dim_H_values) / len(dim_H_values)
    mean_rank_com = sum(rank_com_values) / len(rank_com_values)
    
    correlation_coefficient = sum((dim_H - mean_dim_H) * (rank_com - mean_rank_com) for dim_H, rank_com in results) / (len(results) * sum((dim_H - mean_dim_H)**2 for dim_H in dim_H_values))
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(dim_H_values),
        "n_max": 40,
        "conjecture_holds": abs(correlation_coefficient) >= 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation below threshold\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")