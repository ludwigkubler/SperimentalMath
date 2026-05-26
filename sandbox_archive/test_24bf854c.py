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

def xor_and_tree_width(tree):
    if isinstance(tree, list):
        return max(xor_and_tree_width(subtree) for subtree in tree)
    else:
        return 1

def quandle_structure(tree):
    if isinstance(tree, list):
        left = quandle_structure(tree[0])
        right = quandle_structure(tree[1])
        return set(left).union(right)
    else:
        return {tree}

def minimal_rank(quandle):
    generators = []
    for node in quandle:
        if all(node != g for g in generators):
            generators.append(node)
    return len(generators)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 5 instances per size
            tree = generate_xor_and_tree(n)
            quandle = quandle_structure(tree)
            rank = minimal_rank(quandle)
            tw = xor_and_tree_width(tree)
            results.append((rank, tw))
    
    if not results:
        return {
            "metric_name": "minimal_rank",
            "metric_value": 0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    rank_values = [r for r, _ in results]
    tw_values = [tw for _, tw in results]
    mean_rank = sum(rank_values) / len(rank_values)
    mean_tw = sum(tw_values) / len(tw_values)
    
    if all(r <= c * tw for r, tw in results):
        return {
            "metric_name": "minimal_rank",
            "metric_value": mean_rank,
            "instances_tested": len(results),
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        counterexample = f"rank={max(rank_values)}, expected={max(tw_values) * c}"
        return {
            "metric_name": "minimal_rank",
            "metric_value": mean_rank,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": counterexample
        }

def generate_xor_and_tree(n):
    if n == 1:
        return random.choice([0, 1])
    else:
        left = generate_xor_and_tree(n // 2)
        right = generate_xor_and_tree(n - n // 2)
        return [left, right]

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        result = f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}"
    
    print(result)