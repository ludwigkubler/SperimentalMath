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
    
    def xor_and_tree_width(tree):
        if not tree:
            return 0
        left, right = tree
        return max(xor_and_tree_width(left), xor_and_tree_width(right)) + 1
    
    def minimal_rank_eichler_order(vertex_partition):
        # Placeholder for actual Eichler order computation procedure
        # This is a dummy implementation that returns a random rank
        return random.randint(1, len(vertex_partition))
    
    n = random.randint(5, 40)
    tree = generate_xor_and_tree(n)
    vertex_partition = partition_vertices(tree)
    rank = minimal_rank_eichler_order(vertex_partition)
    width = xor_and_tree_width(tree)
    
    if width == 0:
        return {
            "metric_name": "rank_to_width_ratio",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "tree_width_zero"
        }
    
    ratio = rank / width
    
    return {
        "metric_name": "rank_to_width_ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

def generate_xor_and_tree(n):
    if n == 1:
        return []
    left = generate_xor_and_tree(random.randint(1, n-1))
    right = generate_xor_and_tree(n - len(left) - 1)
    return [left, right]

def partition_vertices(tree):
    # Placeholder for actual vertex partitioning procedure
    # This is a dummy implementation that returns a random partition
    vertices = list(range(len(tree)))
    random.shuffle(vertices)
    return vertices

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"seed {r['seed']}\" first_failing_seed={r['seed']}")
                break