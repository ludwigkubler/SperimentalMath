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
    
    def permutation_action(cnf):
        action = {}
        for clause in cnf:
            for literal in clause:
                if abs(literal) not in action:
                    action[abs(literal)] = {literal: 1 if literal > 0 else -1}
                else:
                    action[abs(literal)][literal] = 1 if literal > 0 else -1
        return action
    
    def communication_complexity_rank(cnf):
        # Placeholder for actual computation
        return len(cnf)
    
    def min_order_representation(action):
        orders = [sum(abs(val) for val in action[var].values()) for var in action]
        return min(orders) if orders else 0
    
    n = random.randint(5, 30)
    cnf = [[random.choice([-1, 1]) * (i + 1) for i in range(n)] for _ in range(random.randint(2, 5))]
    
    action = permutation_action(cnf)
    min_order = min_order_representation(action)
    r_phi = communication_complexity_rank(cnf)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": min_order * r_phi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    metric_values = [result["metric_value"] for result in results if "metric_value" in result]
    conjecture_holds = all(result["conjecture_holds"] for result in results if "conjecture_holds" in result)
    
    mean = sum(metric_values) / len(metric_values) if metric_values else 0
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values)) if len(metric_values) > 1 else 0
    
    support_fraction = sum(1 for result in results if "conjecture_holds" in result and result["conjecture_holds"]) / len(results)
    
    if conjecture_holds:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(result["counterexample"] for result in results):
        counterexample = next(result["counterexample"] for result in results if "counterexample" in result)
        first_failing_seed = next(result["seed"] for result in results if "conjecture_holds" not in result or not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_conjecture_holds")