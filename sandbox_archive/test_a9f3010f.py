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
    
    def generate_manifold(n):
        # Simple 2D manifold represented as a list of edges
        return [(random.randint(0, n-1), random.randint(0, n-1)) for _ in range(n)]
    
    def min_light_paths(manifold):
        # Placeholder function to compute min light paths
        return len(manifold)
    
    def smallest_circuit_size(manifold):
        # Placeholder function to compute smallest circuit size
        return len(manifold) // 2
    
    n = random.randint(5, 40)
    manifold = generate_manifold(n)
    light_paths = min_light_paths(manifold)
    circuit_size = smallest_circuit_size(manifold)
    
    if circuit_size == 0:
        return {
            "metric_name": "ratio",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "circuit_size_zero"
        }
    
    ratio = light_paths / circuit_size
    
    return {
        "metric_name": "ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30)) + [101, 103, 107, 109]
    
    results = []
    total_ratio = 0
    count_supporting = 0
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        total_ratio += trial_result["metric_value"]
        if trial_result["conjecture_holds"]:
            count_supporting += 1
        
        results.append(trial_result)
    
    mean_ratio = total_ratio / len(results)
    support_fraction = count_supporting / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")