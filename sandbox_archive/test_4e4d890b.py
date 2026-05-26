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
    
    def generate_tree(depth, branching_factor):
        if depth == 0:
            return "A"
        else:
            children = [generate_tree(random.randint(1, depth-1), branching_factor) for _ in range(branching_factor)]
            return f"({', '.join(children)})"
    
    def tropicalize(tree):
        if tree == "A":
            return []
        elif ',' not in tree:
            return [tree]
        else:
            children = tree[1:-1].split(', ')
            return [tropicalize(child) for child in children]
    
    def compute_rank(tropicalized_tree):
        if not tropicalized_tree:
            return 0
        rank = 0
        for subtree in tropicalized_tree:
            rank += compute_rank(subtree)
        return rank + len(tropicalized_tree)
    
    depths = [5, 10, 15, 20, 30, 40]
    branching_factors = [2, 3, 4, 5, 6]
    results = []
    
    for depth in depths:
        for _ in range(5):  # Ensure at least 5 instances per seed
            tree = generate_tree(depth, random.choice(branching_factors))
            rank = compute_rank(tropicalize(tree))
            expected_rank = math.ceil((depth ** 1.5) * (random.choice(branching_factors) ** 0.5))
            results.append({
                "depth": depth,
                "branching_factor": random.choice(branching_factors),
                "rank": rank,
                "expected_rank": expected_rank
            })
    
    mean_value = sum(result["rank"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["rank"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if abs(result["rank"] - result["expected_rank"]) <= 0.1 * result["expected_rank"]) / len(results)
    
    conjecture_holds = support_fraction >= 0.8
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")