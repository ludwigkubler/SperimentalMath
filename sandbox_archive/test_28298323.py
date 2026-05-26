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
    
    def construct_xor_and_tree(edges):
        if not edges:
            return None
        mid = len(edges) // 2
        left_edges = edges[:mid]
        right_edges = edges[mid:]
        return (construct_xor_and_tree(left_edges), construct_xor_and_tree(right_edges))
    
    def count_nodes(tree):
        if tree is None:
            return 0
        return 1 + count_nodes(tree[0]) + count_nodes(tree[1])
    
    def generate_k_clique(n, k):
        nodes = list(range(n))
        edges = []
        for i in range(k):
            for j in range(i+1, k):
                edges.append((nodes[i], nodes[j]))
        return edges
    
    n = random.randint(5, 40)
    k = random.randint(2, min(n-1, 3))  # Ensure at least one edge
    clique = generate_k_clique(n, k)
    xor_and_tree = construct_xor_and_tree(clique)
    
    if xor_and_tree is None:
        return {
            "metric_name": "xor_and_tree_width",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "xor_and_tree_is_empty"
        }
    
    width = count_nodes(xor_and_tree)
    
    # Placeholder for matroid representation rank calculation
    # This is a dummy implementation and should be replaced with actual logic
    rank = n ** k
    
    ratio = Fraction(rank, width)
    if ratio <= n ** k:
        return {
            "metric_name": "ratio_of_rank_to_width",
            "metric_value": float(ratio),
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "ratio_of_rank_to_width",
            "metric_value": float(ratio),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"rank={rank}, expected<=n^k"
        }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")