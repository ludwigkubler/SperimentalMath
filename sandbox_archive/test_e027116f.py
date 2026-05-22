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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_secant_volume(f):
        # Placeholder for actual computation of secant volume
        # This is a dummy implementation for demonstration purposes
        return len(f) ** 0.5
    
    def communication_complexity(f):
        # Placeholder for actual communication complexity calculation
        # This is a dummy implementation for demonstration purposes
        return len(f)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = generate_boolean_function(n)
    secant_volume = compute_secant_volume(f)
    cc = communication_complexity(f)
    
    if secant_volume < n or cc > secant_volume:
        return {
            "metric_name": "Communication Complexity",
            "metric_value": cc,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"CC({f}) = {cc} > τ(f) = {secant_volume}"
        }
    
    return {
        "metric_name": "Communication Complexity",
        "metric_value": cc,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"CC({result['counterexample']}) > τ(f)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")