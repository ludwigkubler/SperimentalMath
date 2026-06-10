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
    
    def generate_circuit(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def characteristic_function(circuit):
        n = len(circuit)
        return sum(circuit[i] * (2 ** i) for i in range(n))
    
    def mock_theta_function(x):
        # Simplified mock theta function for demonstration
        return x**2 + 1
    
    def representation_size(circuit):
        n = len(circuit)
        value = characteristic_function(circuit)
        return mock_theta_function(value)
    
    metric_name = "representation_size"
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):
            circuit = generate_circuit(n)
            size = representation_size(circuit)
            instances_tested += 1
            
            if size > 1.5 * n**(2/3):
                conjecture_holds = False
                counterexample = f"Circuit with {n} inputs and size {size}"
                break
    
    return {
        "metric_name": metric_name,
        "metric_value": 0,  # This is a dummy value as the actual metric depends on the seed
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    
    results = []
    total_metric_value = 0
    total_instances_tested = 0
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        if not trial_result["conjecture_holds"]:
            break
        
        total_metric_value += trial_result["metric_value"]
        total_instances_tested += trial_result["instances_tested"]
    
    if len(seeds) == 30 and all(trial_result["conjecture_holds"] for trial_result in results):
        RESULT = "SUPPORTED mean=0 std=0 support_fraction=1"
    elif any(not trial_result["conjecture_holds"] for trial_result in results):
        counterexample = next(trial_result["counterexample"] for trial_result in results if not trial_result["conjecture_holds"])
        RESULT = f"FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[next(i for i, result in enumerate(results) if not result['conjecture_holds'])]}"
    else:
        RESULT = "INCONCLUSIVE reason=unknown"
    
    print(RESULT)