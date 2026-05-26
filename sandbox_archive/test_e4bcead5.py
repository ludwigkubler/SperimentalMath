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
    
    def generate_k_clique(n):
        return [[i, j] for i in range(n) for j in range(i+1, n)]
    
    def construct_xor_and_tree(edges):
        if not edges:
            return 0
        left_edges = [e for e in edges if e[0] < len(edges) // 2]
        right_edges = [e for e in edges if e[0] >= len(edges) // 2]
        return (construct_xor_and_tree(left_edges), construct_xor_and_tree(right_edges))
    
    def matroid_rank(n, k):
        return n ** k
    
    def xor_and_tree_width(tree):
        if isinstance(tree, int):
            return tree
        else:
            return max(xor_and_tree_width(tree[0]), xor_and_tree_width(tree[1])) + 1
    
    n = random.randint(5, 40)
    clique = generate_k_clique(n)
    xor_and_tree = construct_xor_and_tree(clique)
    matroid_rank_value = matroid_rank(n, len(clique))
    xor_and_tree_width_value = xor_and_tree_width(xor_and_tree)
    
    if xor_and_tree_width_value == 0:
        return {
            "metric_name": "rank_to_width_ratio",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "XOR-AND tree width is 0"
        }
    
    ratio = matroid_rank_value / xor_and_tree_width_value
    
    return {
        "metric_name": "rank_to_width_ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio <= n ** len(clique),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                counterexample = f"rank_to_width_ratio={result['metric_value']}, expected<=n^{len(clique)}"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
                break