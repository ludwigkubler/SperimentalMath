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

def generate_xor_and_tree(n, depth):
    if n == 1:
        return [random.choice([0, 1])]
    if depth == 1:
        return [random.choice([0, 1]) for _ in range(n)]
    
    left = generate_xor_and_tree(n // 2, depth - 1)
    right = generate_xor_and_tree(n - n // 2, depth - 1)
    return [left[i] ^ right[i % len(right)] for i in range(n)]

def compute_minimal_rank(tree):
    n = len(tree)
    if n == 1:
        return 1
    
    left = tree[:n // 2]
    right = tree[n // 2:]
    
    rank_left = compute_minimal_rank(left)
    rank_right = compute_minimal_rank(right)
    
    return max(rank_left, rank_right) + 1

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    depth = random.randint(3, 6)
    tree = generate_xor_and_tree(n, depth)
    omega_T = len(tree)
    
    if omega_T < n / 2:
        return {
            "metric_name": "minimal_rank",
            "metric_value": compute_minimal_rank(tree),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "omega(T) < n/2"
        }
    
    rank = compute_minimal_rank(tree)
    ratio = Fraction(rank, omega_T).limit_denominator()
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "conjecture_holds": 0.5 <= ratio <= 1.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    support_count = sum(1 for r in results if r["conjecture_holds"])
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = Fraction(support_count, len(results))
    
    if support_fraction >= Fraction(24, 30):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"omega(T) < n/2\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support")