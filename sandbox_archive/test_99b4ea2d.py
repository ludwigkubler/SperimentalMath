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
    
    def gaussian_mean_variance(n):
        mean = 0
        variance = n
        return mean, variance
    
    def symplectic_leaves_count(n):
        # Simplified model for the number of symplectic leaves
        return 2**n
    
    def action_complexity(n):
        # Simplified model for action complexity
        return math.sqrt(2**(n/2))
    
    def orthogonal_projection(n):
        # Simplified model for orthogonal projection
        return n**2 / 4
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        mean, variance = gaussian_mean_variance(n)
        leaves_count = symplectic_leaves_count(n)
        action_comp = action_complexity(n)
        proj = orthogonal_projection(n)
        
        if leaves_count == 0:
            continue
        
        results.append({
            "n": n,
            "mean": mean,
            "variance": variance,
            "leaves_count": leaves_count,
            "action_comp": action_comp,
            "proj": proj
        })
    
    total_leaves = sum(result["leaves_count"] for result in results)
    avg_action_comp = sum(result["action_comp"] for result in results) / len(results)
    avg_proj = sum(result["proj"] for result in results) / len(results)
    
    metric_value = avg_action_comp
    instances_tested = len(results)
    conjecture_holds = True
    counterexample = ""
    
    if not (mean - 3 * math.sqrt(variance) <= avg_action_comp <= mean + 3 * math.sqrt(variance)):
        conjecture_holds = False
        counterexample = "Action complexity does not follow the Gaussian distribution."
    
    for i in range(len(results)):
        for j in range(i+1, len(results)):
            if results[i]["action_comp"]**2 + results[j]["action_comp"]**2 < (results[i]["n"]**2 / 4):
                conjecture_holds = False
                counterexample = "Inequality E[ρ(f1)^2 + ρ(f2)^2] ≥ (n^2/4) is not satisfied."
    
    return {
        "metric_name": "Action Complexity",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((result["seed"] for result in results if not result["conjecture_holds"]), None)
        counterexample_desc = "Action complexity does not follow the Gaussian distribution or inequality is not satisfied."
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")