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

def generate_xor_and_tree(n, depth):
    if n == 1:
        return [random.choice([0, 1])]
    elif depth == 1:
        return [random.choice([0, 1]) for _ in range(n)]
    
    left = generate_xor_and_tree(n // 2, depth - 1)
    right = generate_xor_and_tree(n - n // 2, depth - 1)
    return [left[i] ^ right[i % len(right)] for i in range(n)]

def compute_minimal_rank(tree):
    if not tree:
        return 0
    elif len(tree) == 1:
        return 1
    
    left_rank = compute_minimal_rank([t[0] for t in tree])
    right_rank = compute_minimal_rank([t[1] for t in tree])
    return max(left_rank, right_rank) + 1

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    depth = random.randint(3, 3)
    tree = generate_xor_and_tree(n, depth)
    omega_T = len(tree)
    
    minimal_rank = compute_minimal_rank(tree)
    ratio = Fraction(minimal_rank, omega_T)
    
    return {
        "metric_name": "minimal_rank_ratio",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "conjecture_holds": 0.5 <= ratio <= 1.5,
        "counterexample": "" if 0.5 <= ratio <= 1.5 else f"Ratio {ratio} out of bounds"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(3, 6)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if 0.5 <= r["metric_value"] <= 1.5) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction support_fraction={support_fraction}")