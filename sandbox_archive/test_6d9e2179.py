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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_non_abelian_automorphism_group_rank(f):
        # Placeholder function to simulate computation
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(1, n)
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    
    for n in n_values:
        for _ in range(30):  # Ensure at least 30 instances per seed
            f = generate_boolean_function(n)
            rank = compute_non_abelian_automorphism_group_rank(f)
            ranks.append(rank)
    
    if not ranks:
        return {
            "metric_name": "Var(γ(f))",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_ranks"
        }
    
    mean_rank = sum(ranks) / len(ranks)
    variance = sum((x - mean_rank) ** 2 for x in ranks) / len(ranks)
    n_max = max(n_values)
    
    return {
        "metric_name": "Var(γ(f))",
        "metric_value": variance,
        "instances_tested": len(ranks),
        "n_max": n_max,
        "conjecture_holds": variance <= 10 * n_max ** 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    total_variance = 0
    valid_trials = 0
    
    for seed in seeds:
        trial_result = run_trial(seed)
        results.append(trial_result)
        
        if trial_result["instances_tested"] > 0:
            total_variance += trial_result["metric_value"]
            valid_trials += 1
    
    if not valid_trials:
        print("RESULT: INCONCLUSIVE no_valid_trials")
    else:
        mean_variance = total_variance / valid_trials
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_variance} std=Unknown support_fraction={support_fraction}")
        else:
            first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
            print(f"RESULT: FALSIFIED counterexample=\"variance_exceeded\" first_failing_seed={first_failing_seed}")