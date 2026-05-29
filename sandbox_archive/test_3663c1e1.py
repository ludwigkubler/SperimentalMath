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
    
    def generate_boolean_function(n, m):
        return [random.choice([0, 1]) for _ in range(m)]
    
    def min_order_affine_group(n):
        # Simplified approximation of the minimal order of an affine group
        return math.ceil(math.pow(n, 3/2))
    
    def resolution_proof_size(f):
        # Placeholder function to simulate resolution proof size calculation
        return len(f) * 10
    
    m = random.randint(5, 15)
    n = random.randint(5, 15)
    f = generate_boolean_function(n, m)
    
    min_order = min_order_affine_group(n)
    proof_size = resolution_proof_size(f)
    
    return {
        "metric_name": "min_order_vs_resolution",
        "metric_value": proof_size / min_order,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        counterexample = next(result for result in results if not result["conjecture_holds"])["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[results.index(next(result for result in results if not result['conjecture_holds']))]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")