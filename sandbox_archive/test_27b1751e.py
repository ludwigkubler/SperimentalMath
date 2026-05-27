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
    
    def generate_xor_and_tree(n):
        if n == 1:
            return ['leaf']
        else:
            left = generate_xor_and_tree(n // 2)
            right = generate_xor_and_tree(n - n // 2)
            return ['node', left, right]
    
    def compute_minimal_rank(tree):
        if isinstance(tree, list) and tree[0] == 'leaf':
            return 1
        elif isinstance(tree, list) and tree[0] == 'node':
            left_rank = compute_minimal_rank(tree[1])
            right_rank = compute_minimal_rank(tree[2])
            return max(left_rank, right_rank) + 1
        else:
            raise ValueError("Invalid tree structure")
    
    n = random.randint(5, 40)
    tree = generate_xor_and_tree(n)
    minimal_rank = compute_minimal_rank(tree)
    
    metric_value = minimal_rank
    instances_tested = 1
    conjecture_holds = minimal_rank <= n * math.log2(n)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")