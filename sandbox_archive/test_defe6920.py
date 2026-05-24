# auto-injected by SEC sandbox
import itertools
import collections
import json
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
import sys

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Define constants and parameters
    c = 2  # Example constant for AC0 parity circuit size
    
    # Generate a random boolean function f with input size n
    n = random.randint(5, 40)
    f = [random.choice([0, 1]) for _ in range(2**n)]
    
    # Compute the tropical geometry property Q (simplified example)
    Q = sum(f) / len(f)
    
    # Construct an AC0 parity circuit C for the function f
    # This is a simplified example; actual implementation depends on the function
    circuit_size = n  # Placeholder value
    
    # Check if property Q holds and if the circuit size satisfies the inequality
    property_Q_holds = abs(Q - 0.5) < 1e-6  # Simplified check
    conjecture_holds = property_Q_holds and circuit_size >= c * math.log(n)
    
    return {
        "metric_name": "circuit_size",
        "metric_value": circuit_size,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Property Q does not hold or circuit size is too small."
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    total_metric_value = 0
    num_seeds_supporting_conjecture = 0
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        results.append(trial_result)
        total_metric_value += trial_result["metric_value"]
        if trial_result["conjecture_holds"]:
            num_seeds_supporting_conjecture += 1
    
    mean_metric_value = Fraction(total_metric_value, len(results))
    support_fraction = Fraction(num_seeds_supporting_conjecture, len(results))
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Property Q does not hold or circuit size is too small.\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")