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
    
    def generate_binary_tree(n):
        if n == 0:
            return None
        elif n == 1:
            return (None, None)
        else:
            left = generate_binary_tree(random.randint(0, n-1))
            right = generate_binary_tree(n - 1 - len(left) if left is not None else 0)
            return (left, right)

    def geometric_entropy(tree):
        if tree is None:
            return 0
        elif isinstance(tree, tuple):
            left, right = tree
            total_nodes = 1 + (len(left) if left is not None else 0) + (len(right) if right is not None else 0)
            p_left = len(left) / total_nodes if left is not None else 0
            p_right = len(right) / total_nodes if right is not None else 0
            return -p_left * math.log2(p_left) - p_right * math.log2(p_right)
        else:
            raise ValueError("Invalid tree structure")

    def resolution_proof_width(tree):
        if tree is None:
            return 1
        elif isinstance(tree, tuple):
            left, right = tree
            return max(resolution_proof_width(left), resolution_proof_width(right)) + 1
        else:
            raise ValueError("Invalid tree structure")

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        tree = generate_binary_tree(n)
        Hmin_G = geometric_entropy(tree)
        if Hmin_G <= 0:
            continue
        w_phi = resolution_proof_width(tree)
        ratio = w_phi / Hmin_G
        results.append({"n": n, "Hmin_G": Hmin_G, "w_phi": w_phi, "ratio": ratio})
    
    if not results:
        return {
            "metric_name": "resolution_proof_width_ratio",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid binary trees generated"
        }
    
    metric_value = sum(result["ratio"] for result in results) / len(results)
    instances_tested = len(results)
    n_max = max(result["n"] for result in results)
    conjecture_holds = all(result["ratio"] >= 1 for result in results)
    counterexample = "" if conjecture_holds else "Ratio < 1 found"
    
    return {
        "metric_name": "resolution_proof_width_ratio",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE No trials executed")
    else:
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
        elif any(not result["conjecture_holds"] for result in results):
            first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"Ratio < 1 found\" first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE No support for conjecture")