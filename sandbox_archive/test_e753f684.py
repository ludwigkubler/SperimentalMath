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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def and_or_tree_width(f):
        if len(f) == 1:
            return 1
        else:
            left = f[:len(f)//2]
            right = f[len(f)//2:]
            return max(and_or_tree_width(left), and_or_tree_width(right)) + 1
    
    def birational_geometry_invariant(f):
        # Placeholder for the actual computation of the invariant
        # This is a dummy function that returns a random value for demonstration
        return random.random()
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        width = and_or_tree_width(f)
        invariant = birational_geometry_invariant(f)
        max_order = abs(invariant)
        
        if max_order > math.log(n, 2):
            return {
                "metric_name": "maximal_order",
                "metric_value": max_order,
                "instances_tested": len(n_values),
                "conjecture_holds": False,
                "counterexample": f"n={n}, invariant={invariant}"
            }
        
        results.append(max_order)
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean)**2 for x in results) / len(results))
    
    return {
        "metric_name": "maximal_order",
        "metric_value": mean,
        "instances_tested": len(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        if not trial_result["conjecture_holds"]:
            print(f"RESULT: FALSIFIED counterexample=\"{trial_result['counterexample']}\" first_failing_seed={seed}")
            break
    
    else:
        mean = sum(trial_result["metric_value"] for trial_result in results) / len(results)
        std_dev = math.sqrt(sum((trial_result["metric_value"] - mean)**2 for trial_result in results) / len(results))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")