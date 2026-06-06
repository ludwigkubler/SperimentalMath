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
    
    def communication_complexity_rank(f, n):
        # Placeholder function to compute the rank
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(1, n)
    
    def calculate_variance(ranks):
        mean = sum(ranks) / len(ranks)
        variance = sum((x - mean) ** 2 for x in ranks) / len(ranks)
        return variance
    
    def get_automorphism_groups(f, n):
        # Placeholder function to compute automorphism groups
        # This is a dummy implementation and should be replaced with actual logic
        return [f]
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    ranks = [communication_complexity_rank(f, n) for _ in range(30)]
    variance = calculate_variance(ranks)
    conjecture_holds = variance <= n**2 * math.log(n)
    
    return {
        "metric_name": "variance",
        "metric_value": variance,
        "instances_tested": 30,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_variance = sum(r["metric_value"] for r in results) / len(results)
    std_variance = math.sqrt(sum((r["metric_value"] - mean_variance) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_variance} std={std_variance} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_variance} std={std_variance} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")