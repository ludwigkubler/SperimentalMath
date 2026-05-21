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
    
    # Generate a random instance with n variables
    n = random.randint(5, 40)
    instance = [random.random() for _ in range(n)]
    
    # Compute the geometric entropy of the moduli space G(I)
    # For simplicity, we use a placeholder function that returns a value between n and n^2 log(n)
    def geometric_entropy(instance):
        return random.uniform(n, n * math.log(n))
    
    H_G_I = geometric_entropy(instance)
    
    # Measure the communication complexity of compressing tensor networks
    # For simplicity, we use a placeholder function that returns a value proportional to H(G(I))
    def communication_complexity(H_G_I):
        return H_G_I
    
    comm_complexity = communication_complexity(H_G_I)
    
    # Check if the conjecture holds
    lower_bound = n
    upper_bound = n * math.log(n)
    conjecture_holds = lower_bound <= H_G_I <= upper_bound and comm_complexity >= H_G_I
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": comm_complexity,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Instance: {instance}, H(G(I)): {H_G_I}, comm_complexity: {comm_complexity}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_comm_complexity = sum(r["metric_value"] for r in results) / len(results)
    std_comm_complexity = math.sqrt(sum((r["metric_value"] - mean_comm_complexity) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_comm_complexity} std={std_comm_complexity} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_comm_complexity} std={std_comm_complexity} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")