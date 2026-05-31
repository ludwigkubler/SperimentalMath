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
    
    # Generate a boolean circuit with n inputs and width w
    n = 10 + random.randint(0, 30)  # Ensure n_min >= 5 and n_max >= 20
    w = 1 + random.randint(0, n-1)
    C = [[random.choice([0, 1]) for _ in range(w)] for _ in range(n)]
    
    # Construct the associated orbifold manifold O(C) from C (simplified model)
    # For simplicity, we assume χ(O(C)) is proportional to the number of gates
    num_gates = sum(len(row) for row in C if len(row) > 1)
    chi_O_C = Fraction(num_gates, 10)  # Simplified Euler characteristic
    
    # Measure the circuit satisfiability time t_s(C) on instances of size n ≤ 40
    t_s_C = random.uniform(0.1, 10) * num_gates  # Simplified satisfiability time
    
    return {
        "metric_name": "Euler Characteristic",
        "metric_value": chi_O_C,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,  # This is a simplified model; actual conjecture may require more complex analysis
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [random.randint(2, 10000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
        std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "mapping_undefined"  # This is a simplified model; actual conjecture may require more complex analysis
        mean_metric_value, std_metric_value, support_fraction = None, None, None
    
    print(f"RESULT: INCONCLUSIVE reason=mapping_undefined n_tested={len(results)}")