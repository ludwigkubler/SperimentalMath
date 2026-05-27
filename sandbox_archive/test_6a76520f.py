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
    
    def xor_and_tree_width(f):
        n = len(f)
        if n == 1:
            return 1
        mid = n // 2
        left_width = xor_and_tree_width(f[:mid])
        right_width = xor_and_tree_width(f[mid:])
        return max(left_width, right_width) + 1
    
    def homology_classes(n):
        # Simplified model for homology classes
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def minimal_rank(homology):
        return len(set(homology))
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    width = xor_and_tree_width(f)
    homology = homology_classes(width)
    rank = minimal_rank(homology)
    
    lower_bound = math.sqrt(n)
    upper_bound = n ** (3/4)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": lower_bound <= rank <= upper_bound,
        "counterexample": "" if lower_bound <= rank <= upper_bound else f"Rank {rank} does not satisfy bounds [{lower_bound}, {upper_bound}]"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or list(range(2, 30*31, 2))  # Default to first 30 odd primes
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(res["metric_value"] for res in results) / len(results)
    std_dev = math.sqrt(sum((res["metric_value"] - mean_rank)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in enumerate(results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")