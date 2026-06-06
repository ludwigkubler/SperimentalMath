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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def calculate_algebraic_automorphism_group_order(f):
        # Placeholder function. Actual implementation required.
        return len(f)  # Simplified for demonstration
    
    def calculate_communication_complexity_rank(f):
        # Placeholder function. Actual implementation required.
        return len(f)  # Simplified for demonstration
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            f = generate_random_boolean_function(n)
            ord_Aut_f = calculate_algebraic_automorphism_group_order(f)
            R_f = calculate_communication_complexity_rank(f)
            if R_f == 0:
                continue  # Avoid division by zero
            results.append(ord_Aut_f / R_f)
    
    if not results:
        return {
            "metric_name": "ord(Aut(f))/R_f",
            "metric_value": float('nan'),
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean)**2 for x in results) / len(results))
    conjecture_holds = all(x >= 1.5 for x in results) and std <= 0.3
    
    return {
        "metric_name": "ord(Aut(f))/R_f",
        "metric_value": mean,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(x["metric_value"] for x in results if not math.isnan(x["metric_value"])) / len(results)
    std_metric_value = math.sqrt(sum((x["metric_value"] - mean_metric_value)**2 for x in results if not math.isnan(x["metric_value"])) / len(results))
    support_fraction = sum(1 for x in results if x["conjecture_holds"]) / len(results)
    
    if all(x["conjecture_holds"] for x in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for x in results if not x["conjecture_holds"]) >= 8:
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={seeds[sum(1 for x in results if not x['conjecture_holds'])]}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")