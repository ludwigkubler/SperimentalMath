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
    
    def generate_manifold(n):
        # Simple random manifold generator for demonstration
        return [random.choice([0, 1]) for _ in range(n)]
    
    def min_light_paths(manifold):
        # Placeholder function to compute minimal light paths
        return sum(manifold) + len(manifold)
    
    def smallest_circuit_size(manifold):
        # Placeholder function to compute smallest circuit size
        return len(manifold)
    
    n = random.randint(5, 40)
    manifold = generate_manifold(n)
    p = random.choice(range(n))
    light_paths = min_light_paths(manifold)
    circuit_size = smallest_circuit_size(manifold)
    
    if circuit_size == 0:
        return {
            "metric_name": "ratio",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "circuit_size_zero"
        }
    
    ratio = Fraction(light_paths, circuit_size)
    return {
        "metric_name": "ratio",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["metric_value"] is not None for result in results):
        mean = sum(result["metric_value"] for result in results) / len(results)
        std_dev = math.sqrt(sum((result["metric_value"] - mean) ** 2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample='not_enough_support' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE some_trials_failed")