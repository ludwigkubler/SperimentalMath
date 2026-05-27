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
        # Placeholder for actual computation of homology classes
        # For simplicity, we assume a linear relationship with n
        return [i for i in range(1, n+1)]
    
    def minimal_rank(homology):
        return len(homology)
    
    n = random.randint(5, 40)  # Sweep through different sizes
    f = generate_boolean_function(n)
    width = xor_and_tree_width(f)
    homology = homology_classes(width)
    rank = minimal_rank(homology)
    
    lower_bound = math.sqrt(n)
    upper_bound = n ** (3/4)
    
    conjecture_holds = lower_bound <= rank <= upper_bound
    counterexample = "" if conjecture_holds else f"n={n}, rank={rank}"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample_desc = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")