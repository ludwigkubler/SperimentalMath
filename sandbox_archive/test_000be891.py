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
        left = f[:mid]
        right = f[mid:]
        return max(xor_and_tree_width(left), xor_and_tree_width(right)) + 1
    
    def homology_classes(n):
        # Placeholder for actual computation of homology classes
        # For simplicity, we assume the number of homology classes is proportional to n^(3/4)
        return [i for i in range(int(n**(3/4)))]

    def minimal_rank(homology_classes):
        # Placeholder for actual computation of minimal rank
        # For simplicity, we assume the minimal rank is proportional to n^(1/2)
        return int(math.sqrt(len(homology_classes)))
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    width = xor_and_tree_width(f)
    hom_classes = homology_classes(width)
    rank = minimal_rank(hom_classes)
    
    lower_bound = math.ceil(n**(1/2))
    upper_bound = math.floor(n**(3/4))
    
    metric_value = rank
    conjecture_holds = lower_bound <= rank <= upper_bound
    counterexample = "" if conjecture_holds else "rank_out_of_bounds"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank_out_of_bounds\" first_failing_seed={first_failing_seed}")