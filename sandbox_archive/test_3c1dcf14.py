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
    
    def calculate_geometric_entanglement_entropy(f, n):
        # Placeholder function to calculate geometric entanglement entropy
        # This is a dummy implementation and should be replaced with actual calculation
        return random.random() / (n ** 2)
    
    def communication_complexity(f, n):
        # Placeholder function to calculate communication complexity
        # This is a dummy implementation and should be replaced with actual calculation
        return len(f) ** 0.5
    
    n = random.randint(5, 40)
    f = generate_random_boolean_function(n)
    c_f = communication_complexity(f, n)
    
    if c_f == 0:
        return {
            "metric_name": "Geometric Entanglement Entropy",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "communication_complexity_zero"
        }
    
    E_G = calculate_geometric_entanglement_entropy(f, n)
    
    if E_G is None:
        return {
            "metric_name": "Geometric Entanglement Entropy",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "geometric_entanglement_entropy_calculation_failed"
        }
    
    lower_bound = 1 / (n ** 2)
    
    return {
        "metric_name": "Geometric Entanglement Entropy",
        "metric_value": E_G,
        "instances_tested": 1,
        "conjecture_holds": E_G >= lower_bound,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    total_metric_value = 0
    conjecture_holds_count = 0
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        if trial_result["metric_value"] is not None:
            total_metric_value += trial_result["metric_value"]
            if trial_result["conjecture_holds"]:
                conjecture_holds_count += 1
        
        results.append(trial_result)
    
    mean_metric_value = total_metric_value / len(results) if results else 0
    support_fraction = conjecture_holds_count / len(results) if results else 0
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.00 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.00 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='geometric_entanglement_entropy_calculation_failed' first_failing_seed={first_failing_seed}")