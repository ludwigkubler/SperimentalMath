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
    if depth == 1:
        return [random.choice([0, 1]) for _ in range(n)]
    
    left = generate_xor_and_tree(n // 2, depth - 1)
    right = generate_xor_and_tree(n - n // 2, depth - 1)
    return [left[i] ^ right[i % len(right)] for i in range(n)]

def compute_minimal_rank(tree):
    if not tree:
        return 0
    if len(tree) == 1:
        return 1
    
    left_rank = compute_minimal_rank([node[0] for node in tree])
    right_rank = compute_minimal_rank([node[1] for node in tree])
    
    return max(left_rank, right_rank) + 1

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    depth = random.randint(3, 6)
    tree = generate_xor_and_tree(n, depth)
    
    minimal_rank = compute_minimal_rank(tree)
    omega_T = len(tree)
    
    if omega_T < n / 2:
        ratio = Fraction(minimal_rank, omega_T)
        conjecture_holds = 0.5 <= ratio <= 1.5
        counterexample = "" if conjecture_holds else f"Ratio {ratio} out of bounds"
    else:
        conjecture_holds = False
        counterexample = "Tree width not less than n/2"
    
    return {
        "metric_name": "minimal_rank_ratio",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={math.sqrt(sum((r['metric_value'] - mean_ratio) ** 2 for r in results) / len(results))} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Tree width not less than n/2\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")