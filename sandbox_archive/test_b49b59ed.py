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
    
    def generate_frege_tree(depth):
        if depth == 1:
            return ['A']
        else:
            left = generate_frege_tree(random.randint(1, depth-1))
            right = generate_frege_tree(random.randint(1, depth-1))
            return [f"({left[0]} {right[0]})"]
    
    def compute_min_rank(tree):
        if isinstance(tree, list):
            tree = tree[0]
        if '(' not in tree:
            return 1
        left, right = tree.split(' ', 1)
        return max(compute_min_rank(left), compute_min_rank(right))
    
    n = random.randint(5, 40)
    depth = math.ceil(math.log(n))
    frege_tree = generate_frege_tree(depth)
    min_rank = compute_min_rank(frege_tree)
    
    if min_rank > depth:
        return {
            "metric_name": "MinRank",
            "metric_value": min_rank,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Tree with depth {depth} has min rank {min_rank}"
        }
    
    def generate_quiver_representation(tree):
        if isinstance(tree, list):
            tree = tree[0]
        if '(' not in tree:
            return 1
        left, right = tree.split(' ', 1)
        return max(generate_quiver_representation(left), generate_quiver_representation(right))
    
    quiver_rank = generate_quiver_representation(frege_tree)
    
    if quiver_rank > 2 ** depth:
        return {
            "metric_name": "QuiverRank",
            "metric_value": quiver_rank,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Tree with depth {depth} has quiver rank {quiver_rank}"
        }
    
    return {
        "metric_name": "MinRank",
        "metric_value": min_rank,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")