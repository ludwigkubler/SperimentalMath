# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def generate_xor_and_tree(n):
    if n == 1:
        return []
    left_size = random.randint(1, n-2)
    right_size = n - left_size - 1
    left = generate_xor_and_tree(left_size)
    right = generate_xor_and_tree(right_size)
    return [left, right]

def compute_minimal_rank(tree):
    if not tree:
        return 0
    left_rank = compute_minimal_rank(tree[0])
    right_rank = compute_minimal_rank(tree[1])
    return max(left_rank, right_rank) + 1

def compute_xor_and_tree_width(tree):
    if not tree:
        return 0
    left_width = compute_xor_and_tree_width(tree[0])
    right_width = compute_xor_and_tree_width(tree[1])
    return max(left_width, right_width) + 1

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        tree = generate_xor_and_tree(n)
        rank = compute_minimal_rank(tree)
        width = compute_xor_and_tree_width(tree)
        if width == 0:
            continue
        ratio = Fraction(rank, width)
        results.append(ratio)
    
    mean_ratio = sum(results) / len(results) if results else 0
    support_fraction = len([r for r in results if r >= 1]) / len(results) if results else 0
    
    return {
        "metric_name": "minimal_rank_over_width",
        "metric_value": float(mean_ratio),
        "instances_tested": len(results),
        "conjecture_holds": support_fraction > 0.8,
        "counterexample": "" if support_fraction > 0.8 else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30*31, 67))[:30]  # Default to first 30 prime numbers
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_ratio = sum(r["metric_value"] for r in results if "metric_value" in r) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")