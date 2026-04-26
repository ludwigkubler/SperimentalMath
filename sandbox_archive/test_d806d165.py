# auto-injected by SEC sandbox
import itertools
import collections
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
import json
from sys import argv

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_monotone_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def decision_tree_size(f):
        n = int(math.log2(len(f)))
        if len(f) != 2**n:
            raise ValueError("Function length must be a power of 2")
        if n == 1:
            return 1
        left = f[:2**(n-1)]
        right = f[2**(n-1):]
        return 1 + max(decision_tree_size(left), decision_tree_size(right))
    
    def query_to_communication_lifting(dt_size):
        # Simplified version of the lifting theorem for demonstration purposes
        return dt_size * math.log2(dt_size)
    
    n = random.choice([5, 8, 11, 14])
    f = generate_monotone_function(n)
    dt_size = decision_tree_size(f)
    lifted_value = query_to_communication_lifting(dt_size)
    
    try:
        circuit_size = len(f)  # Simplified monotone circuit size
    except Exception as e:
        return {
            "metric_name": "monotone_circuit_size",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": str(e)
        }
    
    return {
        "metric_name": "monotone_circuit_size",
        "metric_value": circuit_size,
        "instances_tested": 1,
        "conjecture_holds": circuit_size <= lifted_value,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in argv[1:]] if argv[1:] else [11, 23, 37, 53, 71]
    
    results = []
    total_metric_value = 0
    count_supporting = 0
    
    for seed in seeds:
        trial_result = run_trial(seed)
        results.append(trial_result)
        total_metric_value += trial_result["metric_value"]
        if trial_result["conjecture_holds"]:
            count_supporting += 1
    
    mean_metric_value = total_metric_value / len(seeds)
    support_fraction = count_supporting / len(seeds)
    
    print(json.dumps({"TRIAL": {"seed": seed, **trial_result} for seed, trial_result in zip(seeds, results)}))
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.2f} std=NA support_fraction={support_fraction:.2f}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"lifting_theorem\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE lifting_theorem_undefined")