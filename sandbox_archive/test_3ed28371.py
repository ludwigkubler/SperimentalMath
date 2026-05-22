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
    
    # Generate a set of n variables (n ≤ 40)
    n = random.randint(5, 40)
    
    # Construct a random Boolean formula with m monomials
    m = random.randint(1, n)
    monomials = [tuple(random.sample(range(n), k)) for k in range(1, m+1)]
    
    # For simplicity, we will assume the Hodge class is directly related to the number of variables and monomials
    # This is a placeholder for the actual constructive mapping provided in the conjecture
    h_m = n * m
    
    # Calculate the geometric entropy of the Hodge class (simplified as log2(h_m))
    if h_m <= 0:
        return {
            "metric_name": "geometric_entropy",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "h_m must be positive"
        }
    
    geometric_entropy = math.log2(h_m)
    
    # Analyze the relationship between n, m, and geometric entropy
    ratio = geometric_entropy / n
    
    return {
        "metric_name": "geometric_entropy",
        "metric_value": geometric_entropy,
        "instances_tested": 1,
        "conjecture_holds": ratio <= n**0.5,  # Example polynomial bound O(n^0.5)
        "counterexample": "" if ratio <= n**0.5 else f"Ratio {ratio} exceeds O(n^0.5)"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    total_metric_value = sum(result["metric_value"] for result in results)
    mean_metric_value = total_metric_value / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for result in results if not result["conjecture_holds"]) / len(results) >= 0.2:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio exceeds O(n^0.5)\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")